"""One publication boundary for reader, catalog, search, citations and resources."""
import copy
import hashlib
import re
from html import unescape
import nh3
from django.db import transaction
from django.utils import timezone
from ..models import Topic, TopicPublication, LearningResource, TopicRelation
from ..exceptions import ServiceError

TAGS = set('h1 h2 h3 h4 h5 h6 p br hr div span strong em b i u s del ins mark small sub sup blockquote q cite abbr pre code kbd samp var ul ol li dl dt dd a figure figcaption table caption colgroup col thead tbody tfoot tr th td'.split())
ATTRS = {'*': {'title', 'lang', 'dir'}, 'a': {'href'}, 'th': {'scope', 'colspan', 'rowspan'}, 'td': {'colspan', 'rowspan'}, 'ol': {'start', 'reversed'}, 'li': {'value'}}


def sanitize(html):
    # No arbitrary remote images in publication HTML; image blocks have protected routes.
    return nh3.clean(html, tags=TAGS, attributes=ATTRS, url_schemes={'https', 'http', 'mailto'}, link_rel='noopener noreferrer')


def plain(html):
    return re.sub(r'\s+', ' ', unescape(nh3.clean(html.replace('><', '> <'), tags=set()))).strip()


def visible_publications():
    from django.db.utils import OperationalError, ProgrammingError
    try:
        rows = list(TopicPublication.objects.filter(is_published=True).select_related('topic').order_by('topic__order', 'topic_id')[:5000])
    except (OperationalError, ProgrammingError):
        return {}
    by_id = {p.topic_id: p for p in rows}
    def visible(pub):
        seen = set(); current = pub
        for _ in range(32):
            if current.topic_id in seen: return False
            seen.add(current.topic_id)
            snapshot = current.snapshot
            if current.topic.slug != snapshot.get('slug') or current.topic.parent_id != snapshot.get('parent_id'): return False
            parent_id = snapshot.get('parent_id')
            if parent_id is None: return True
            current = by_id.get(parent_id)
            if current is None: return False
        return False
    approved_edges = set(TopicRelation.objects.filter(status='approved').values_list('source_id', 'target_id', 'kind'))
    for pub in rows:
        pub.snapshot = copy.deepcopy(pub.snapshot)
        pub.snapshot['relations'] = [r for r in pub.snapshot.get('relations', [])
                                     if (pub.topic_id, r['target_id'], r['kind']) in approved_edges]
    return {p.topic_id: p for p in rows if visible(p)}


def resolve_publication(slug):
    publications = visible_publications()
    pub = next((p for p in publications.values() if p.snapshot.get('slug') == slug), None)
    if pub is None:
        raise ServiceError('topic_unavailable', 'This topic is not currently published.', 404)
    return pub, publications


def summary(pub, publications, quiz_topics=None):
    has_quiz = (pub.topic_id in quiz_topics) if quiz_topics is not None else False
    return {'id': pub.topic_id, 'title': pub.title, 'slug': pub.snapshot['slug'], 'revision': pub.revision,
            'has_children': any(p.snapshot.get('parent_id') == pub.topic_id for p in publications.values()),
            'is_published': True, 'has_notes': bool(pub.snapshot.get('blocks')),
            'has_quiz': has_quiz, 'has_resources': bool(pub.snapshot.get('resource_ids')),
            'is_bookmarked': False, 'is_completed': False}


def detail(pub, publications, user=None):
    from .student import owned_status, eligible_publications
    bookmarks, completed = owned_status(user, publications)
    data = summary(pub, publications)
    data.update(is_bookmarked=pub.topic_id in bookmarks, is_completed=pub.topic_id in completed, is_learning_unit=pub.topic_id in eligible_publications(publications))
    data['blocks'] = copy.deepcopy(pub.snapshot.get('blocks', []))
    for block in data['blocks']:
        block.pop('file_name', None); block.pop('file_hash', None)
        if block.get('block_type') != 'image':
            # Historical raw attachments stay stored; PDFs require resource review.
            block['file'] = None
    data['children'] = [summary(p, publications) for p in publications.values() if p.snapshot.get('parent_id') == pub.topic_id]
    path = []; node = pub
    while node:
        path.append(summary(node, publications)); node = publications.get(node.snapshot.get('parent_id'))
    data['breadcrumbs'] = list(reversed(path))
    from .discovery import related_topics, article_links, article_tags
    data['related'] = related_topics(pub, publications)
    data['keyword_links'] = article_links(pub, publications)
    data['tags'] = article_tags(pub)
    ids = pub.snapshot.get('resource_ids', [])
    resources = LearningResource.objects.filter(id__in=ids, topic_id=pub.topic_id, status='approved').order_by('pk')
    data['resources'] = [{'id': r.pk, 'title': r.title, 'page_count': r.page_count, 'url': f'/resources/{r.pk}?page=1'} for r in resources]
    from .quiz import select_reviewed_quiz, QuizServiceError
    try:
        select_reviewed_quiz(pub.snapshot['slug'])
        data['has_quiz'] = True
    except QuizServiceError:
        data['has_quiz'] = False
    data['published_at'] = pub.published_at
    data['status'] = 'published'
    return data


def get_syllabus_tree(published_only=False, include_tree=False, user=None):
    from ..models import QuizReview
    from django.db.utils import OperationalError, ProgrammingError
    pubs = visible_publications()
    try:
        quiz_topics = set(QuizReview.objects.filter(is_approved=True).values_list('quiz__topic_id', flat=True))
    except (OperationalError, ProgrammingError):
        quiz_topics = set()

    from .student import owned_status
    user_bookmarks, user_completed = owned_status(user, pubs)

    if published_only:
        def pub_node(pub):
            row = summary(pub, pubs, quiz_topics=quiz_topics)
            row['is_bookmarked'] = pub.topic_id in user_bookmarks
            row['is_completed'] = pub.topic_id in user_completed
            if include_tree:
                row['children'] = [pub_node(child) for child in pubs.values() if child.snapshot.get('parent_id') == pub.topic_id]
            return row
        return [pub_node(p) for p in pubs.values() if p.snapshot.get('parent_id') is None]

    topics = list(Topic.objects.all().order_by('order', 'id'))
    children_by_parent = {}
    for t in topics:
        children_by_parent.setdefault(t.parent_id, []).append(t)

    def topic_node(topic):
        pub = pubs.get(topic.id)
        children = children_by_parent.get(topic.id, [])
        is_pub = pub is not None
        node = {
            'id': topic.id,
            'title': pub.title if is_pub else topic.title,
            'slug': pub.snapshot.get('slug', topic.slug) if is_pub else topic.slug,
            'revision': pub.revision if is_pub else None,
            'has_children': bool(children),
            'is_published': is_pub,
            'has_notes': bool(is_pub and pub.snapshot.get('blocks')),
            'has_quiz': (topic.id in quiz_topics) if is_pub else False,
            'has_resources': bool(is_pub and pub.snapshot.get('resource_ids')),
            'is_bookmarked': topic.id in user_bookmarks,
            'is_completed': topic.id in user_completed,
        }
        if include_tree:
            node['children'] = [topic_node(c) for c in children]
        return node

    roots = children_by_parent.get(None, [])
    return [topic_node(r) for r in roots]



def draft_snapshot(topic):
    seen = {topic.pk}; node = topic
    for _ in range(32):
        if not node.parent_id: break
        if node.parent_id in seen: raise ServiceError('invalid_hierarchy', 'Topic hierarchy contains a cycle.')
        seen.add(node.parent_id); node = node.parent
    else: raise ServiceError('invalid_hierarchy', 'Topic hierarchy is too deep.')
    blocks = []
    for block in topic.blocks.order_by('order', 'pk')[:101]:
        if len(block.content) > 100000: raise ServiceError('content_too_large', 'Split large notes into smaller blocks.')
        item = {'id': block.pk, 'block_type': block.block_type, 'content': sanitize(block.content) if block.block_type == 'text' else block.content,
                'order': block.order, 'anchor': f'block-{block.pk}', 'alt_text': block.alt_text, 'caption': block.caption, 'source_reference': block.source_reference, 'file': None}
        if block.file:
            import os
            item.update(
                file=block.file.url,
                file_name=os.path.basename(block.file.name),
                is_pdf=bool(block.block_type == 'pdf' or block.file.name.lower().endswith('.pdf'))
            )
        if block.block_type == 'image' and block.file:
            from ..validators import validate_image
            with block.file.open('rb') as uploaded:
                validate_image(uploaded)
                uploaded.seek(0); file_hash = hashlib.sha256(uploaded.read()).hexdigest()
            if not block.alt_text: raise ServiceError('missing_alt', 'Images require alternative text.')
            item.update(file=f'/api/topic/{topic.slug}/images/{block.pk}/', file_name=block.file.name, file_hash=file_hash)
        blocks.append(item)
    if len(blocks) > 100: raise ServiceError('content_too_large', 'A topic may contain at most 100 blocks.')
    if sum(len(b['content']) for b in blocks) > 500000: raise ServiceError('content_too_large', 'Topic content exceeds publication limit.')
    relations = list(topic.relations.filter(status='approved').order_by('pk').values('target_id', 'kind', 'reason')[:20])
    return {'version': 1, 'title': topic.title, 'slug': topic.slug, 'parent_id': topic.parent_id, 'blocks': blocks,
            'relations': relations, 'tags': list(topic.tags.order_by('pk').values('id', 'name', 'slug')),
            'resource_ids': list(topic.resources.filter(status='approved').values_list('pk', flat=True)[:20])}


@transaction.atomic
def publish(topic, reviewer):
    snapshot = draft_snapshot(topic)
    current = TopicPublication.objects.filter(topic=topic).first()
    if current and (current.snapshot.get('slug') != topic.slug or current.snapshot.get('parent_id') != topic.parent_id):
        raise ServiceError('stable_location_required', 'Published topic locations cannot change without a reviewed migration.')
    if topic.parent_id and topic.parent_id not in visible_publications():
        raise ServiceError('parent_unpublished', 'Publish the reviewed parent first.')
    if any(b['block_type'] == 'text' and b['content'] and not b['source_reference'].strip() for b in snapshot['blocks']):
        raise ServiceError('source_required', 'Text blocks require source references before review/publication.')
    previous = {'revision': current.revision, 'snapshot': current.snapshot} if current else None
    text = ' '.join(plain(b['content']) for b in snapshot['blocks'] if b['block_type'] in ('text', 'heading'))
    publication = TopicPublication.objects.update_or_create(topic=topic, defaults={
        'snapshot': snapshot, 'previous_snapshot': previous, 'revision': current.revision + 1 if current else 1,
        'title': topic.title, 'search_text': text, 'is_published': True, 'published_at': timezone.now(), 'published_by': reviewer,
    })[0]
    publication.tags.set(t['id'] for t in snapshot['tags'])
    Topic.objects.filter(pk=topic.pk).update(editorial_status='draft')
    from .connections import publication_changed
    publication_changed(publication)
    return publication


@transaction.atomic
def republish_previous(publication, reviewer):
    previous = publication.previous_snapshot
    if not previous: raise ServiceError('no_previous_revision', 'No previous publication is available.')
    prior = previous['snapshot']
    publication.previous_snapshot = {'revision': publication.revision, 'snapshot': publication.snapshot}
    publication.snapshot = prior; publication.title = prior['title']
    publication.search_text = ' '.join(plain(b['content']) for b in prior['blocks'] if b['block_type'] in ('text', 'heading'))
    publication.revision += 1; publication.is_published = True
    publication.published_at = timezone.now(); publication.published_by = reviewer
    publication.save()
    publication.tags.set(t['id'] for t in prior.get('tags', []))

    from .connections import publication_changed
    publication_changed(publication)
