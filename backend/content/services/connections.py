"""Bounded Admin-only phrase analysis; reader requests only consume stored decisions."""
import hashlib
from bisect import bisect_left
import json
import unicodedata
from html.parser import HTMLParser
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from ..exceptions import ServiceError
from ..models import TopicAlias, KeywordLinkProposal, ConnectionScan, normalized_label

SKIP = {'a', 'pre', 'code', 'kbd', 'samp', 'script', 'style', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
VOID = {'br', 'hr', 'col', 'img', 'input', 'wbr', 'meta', 'link'}
STOP = {'the', 'and', 'topic', 'notes', 'lesson', 'introduction', 'summary'}
MAX_TERMS = 5000


def meaningful(phrase):
    return 3 <= len(phrase) <= 255 and phrase not in STOP and any(c.isalpha() for c in phrase)


def vocabulary(publications):
    """An ambiguous phrase is excluded, never resolved by arbitrary query order."""
    candidates = {}
    readable = set()
    for pub in publications.values():
        if not pub.search_text or not any(b.get('block_type') == 'text' for b in pub.snapshot.get('blocks', [])):
            continue
        readable.add(pub.topic_id)
        key = normalized_label(pub.title)
        if meaningful(key): candidates.setdefault(key, set()).add(pub.topic_id)
    for topic_id, name in TopicAlias.objects.filter(status='approved', topic_id__in=publications).values_list('topic_id', 'name'):
        key = normalized_label(name)
        if topic_id in readable and meaningful(key):
            candidates.setdefault(key, set()).add(topic_id)
    return {key: next(iter(ids)) for key, ids in candidates.items() if len(ids) == 1}


class ArticleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.nodes = []; self.index = 0

    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack: self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]

    def handle_data(self, text):
        if text:
            if not SKIP.intersection(self.stack): self.nodes.append((self.index, text))
            self.index += 1


def word_character(char):
    return char == '_' or char.isalnum() or unicodedata.category(char).startswith('M')


def folded_offsets(text):
    """NFKC/casefold/whitespace with offsets back to the exact original Unicode."""
    output = []; offsets = []; i = 0
    while i < len(text):
        end = i + 1
        while end < len(text) and unicodedata.category(text[end]).startswith('M'): end += 1
        for char in unicodedata.normalize('NFKC', text[i:end]).casefold():
            char = ' ' if char.isspace() else char
            if char == ' ' and output and output[-1] == ' ':
                offsets[-1] = (offsets[-1][0], end)
            else:
                output.append(char); offsets.append((i, end))
        i = end
    return ''.join(output), offsets


def make_trie(terms):
    trie = {}
    for phrase, target in terms.items():
        branch = trie
        for char in phrase: branch = branch.setdefault(char, {})
        branch[None] = (phrase, target)
    return trie


def find_matches(text, terms, trie=None):
    trie = trie if trie is not None else make_trie(terms)
    folded, offsets = folded_offsets(text)
    utf16 = [0]
    for char in text: utf16.append(utf16[-1] + (2 if ord(char) > 0xffff else 1))
    for start in range(len(folded)):
        if start and word_character(folded[start - 1]): continue
        branch = trie; end = start
        while end < len(folded) and folded[end] in branch:
            branch = branch[folded[end]]; end += 1
            if None in branch and (end == len(folded) or not word_character(folded[end])):
                a, b = offsets[start][0], offsets[end - 1][1]
                key, target = branch[None]
                if b - a > 255: continue
                yield key, target, {'start': utf16[a], 'end': utf16[b], 'text': text[a:b]}, text[max(0, a-90):min(len(text), b+90)]


def source_hash(publication):
    data = [[b.get('id'), b.get('block_type'), b.get('content', '')] for b in publication.snapshot.get('blocks', [])]
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


@transaction.atomic
def suggest_connections(topic, publications=None):
    from .publication import visible_publications
    publications = publications if publications is not None else visible_publications()
    pub = publications.get(topic.pk)
    if pub is None: raise ServiceError('topic_unavailable', 'Publish this article before suggesting connections.', 404)
    terms = {key: target for key, target in vocabulary(publications).items() if target != topic.pk}
    if len(terms) > MAX_TERMS: raise ServiceError('connection_registry_limit', 'Reduce the eligible alias registry before regenerating connections.')
    digest = source_hash(pub); found = {}; trie = make_trie(terms)
    for block in pub.snapshot.get('blocks', []):
        if block.get('block_type') != 'text': continue
        parser = ArticleText(); parser.feed(block.get('content', ''))
        for index, text in parser.nodes:
            for key, target, occurrence, context in find_matches(text, terms, trie):
                record = found.setdefault((key, target), {'phrase': occurrence['text'], 'context': context[:500], 'occurrences': []})
                if len(record['occurrences']) < 8:
                    record['occurrences'].append({**occurrence, 'block_id': block['id'], 'node_index': index})
    # Decisions are immutable across the same evidence; new article HTML gets new
    # pending records, leaving prior approvals/rejections available in Admin.
    KeywordLinkProposal.objects.bulk_create([
        KeywordLinkProposal(source_id=topic.pk, target_id=target, phrase_key=key, source_hash=digest, source_revision=pub.revision, **record)
        for (key, target), record in found.items()
    ], update_conflicts=True, unique_fields=['source', 'target', 'phrase_key', 'source_hash'], update_fields=['source_revision', 'occurrences'])
    ConnectionScan.objects.update_or_create(publication_id=pub.pk, defaults={'pending': False, 'source_revision': pub.revision, 'source_hash': digest, 'analyzed_at': timezone.now()})
    refresh_link_plan(pub, publications)
    return len(found)


def queue_connections():
    """One cheap invalidation on vocabulary changes; no matching on public GET."""
    ConnectionScan.objects.update(pending=True)


def process_pending(limit=20):
    from .publication import visible_publications
    publications = visible_publications()
    pending = list(ConnectionScan.objects.filter(pending=True, publication__is_published=True).select_related('publication__topic').order_by(F('analyzed_at').asc(nulls_first=True), 'pk')[:limit])
    for scan in pending:
        if scan.publication.topic_id in publications:
            suggest_connections(scan.publication.topic, publications)
    return len(pending)


def publication_changed(publication):
    ConnectionScan.objects.get_or_create(publication=publication)
    queue_connections()
    suggest_connections(publication.topic)
    process_pending(max(0, getattr(settings, 'CONNECTION_SCAN_BATCH', 20) - 1))


def decide(proposal, status, reviewer, *, publications=None, terms=None, refresh=True):
    from .publication import visible_publications
    pubs = publications if publications is not None else visible_publications(); pub = pubs.get(proposal.source_id)
    if status != 'rejected' and (status not in ('approved', 'rejected') or pub is None or proposal.source_revision != pub.revision
            or proposal.source_hash != source_hash(pub)
            or (terms if terms is not None else vocabulary(pubs)).get(proposal.phrase_key) != proposal.target_id):
        raise ServiceError('stale_connection', 'This proposal is no longer current. Suggest Connections again and review current evidence.')
    proposal.status = status; proposal.reviewed_by = reviewer; proposal.reviewed_at = timezone.now()
    proposal.save(update_fields=['status', 'reviewed_by', 'reviewed_at'])
    if refresh and pub is not None: refresh_link_plan(pub, pubs)


def compute_link_plan(pub, publications):
    terms = vocabulary(publications)
    hashes = ConnectionScan.objects.filter(publication_id=pub.pk, source_revision=pub.revision).values('source_hash')
    rows = KeywordLinkProposal.objects.filter(source_id=pub.topic_id, source_revision=pub.revision, source_hash__in=hashes, status='approved').order_by('pk')
    candidates = []
    block_order = {b['id']: i for i, b in enumerate(pub.snapshot.get('blocks', []))}
    for row in rows:
        if row.target_id == pub.topic_id or row.target_id not in publications or terms.get(row.phrase_key) != row.target_id: continue
        for occurrence in row.occurrences:
            if occurrence.get('block_id') in block_order:
                candidates.append({**occurrence, 'target_id': row.target_id, 'proposal_id': row.pk})
    # Longest approved phrase wins overlaps. Count/target limits apply globally,
    # across every text block in the article, not separately per component.
    chosen = []; occupied = {}
    for item in sorted(candidates, key=lambda o: (-(o['end']-o['start']), block_order[o['block_id']], o['node_index'], o['start'], o['target_id'])):
        spans = occupied.setdefault((item['block_id'], item['node_index']), [])
        position = bisect_left(spans, (item['start'],))
        if position and spans[position - 1][1] > item['start']: continue
        if position < len(spans) and spans[position][0] < item['end']: continue
        spans.insert(position, (item['start'], item['end']))
        chosen.append(item)
    chosen.sort(key=lambda o: (block_order[o['block_id']], o['node_index'], o['start']))
    unique = []; targets = set()
    for item in chosen:
        if item['target_id'] not in targets:
            unique.append(item); targets.add(item['target_id'])
    return unique[:getattr(settings, 'ARTICLE_LINK_LIMIT', 8)]


def refresh_link_plan(pub, publications):
    plan = compute_link_plan(pub, publications)
    ConnectionScan.objects.filter(publication_id=pub.pk, source_revision=pub.revision, source_hash=source_hash(pub)).update(active_links=plan)


def approved_links(pub, publications):
    """Read at most eight preselected spans; live-check every mutable boundary."""
    scan = ConnectionScan.objects.filter(publication_id=pub.pk, source_revision=pub.revision).first()
    if scan is None: return []
    plan = scan.active_links[:getattr(settings, 'ARTICLE_LINK_LIMIT', 8)]
    rows = KeywordLinkProposal.objects.filter(pk__in=[x['proposal_id'] for x in plan], source_id=pub.topic_id,
        source_revision=pub.revision, source_hash=scan.source_hash, status='approved').values('pk', 'phrase_key', 'target_id')
    reviewed = {r['pk']: r for r in rows}
    terms = vocabulary(publications)
    return [item for item in plan if item['proposal_id'] in reviewed and item['target_id'] != pub.topic_id
            and item['target_id'] in publications and reviewed[item['proposal_id']]['target_id'] == item['target_id']
            and terms.get(reviewed[item['proposal_id']]['phrase_key']) == item['target_id']]
