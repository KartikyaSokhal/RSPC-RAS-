"""Publication-only discovery. No shared caches or content analysis on public GET."""
import math
from ..models import Tag, TopicPublication
from ..exceptions import ServiceError
from .publication import plain


def article_card(pub, publications):
    path = []; node = pub
    while node:
        path.append({'id': node.topic_id, 'title': node.title, 'slug': node.snapshot['slug']})
        node = publications.get(node.snapshot.get('parent_id'))
    return {'id': pub.topic_id, 'title': pub.title, 'slug': pub.snapshot['slug'], 'syllabus_location': list(reversed(path)),
            'read_minutes': max(1, math.ceil(len(pub.search_text.split()) / 200)) if pub.search_text.strip() else None}


def description(pub):
    for block in pub.snapshot.get('blocks', []):
        if block.get('block_type') == 'text':
            text = plain(block.get('content', ''))
            if text: return text[:240] + ('…' if len(text) > 240 else '')
    return ''


def related_topics(pub, publications):
    result = []; used = {pub.topic_id}
    def add(target_id, kind, reason):
        target = publications.get(target_id)
        if target and target_id not in used:
            used.add(target_id)
            result.append({**article_card(target, publications), 'kind': kind, 'reason': reason})
    for edge in pub.snapshot.get('relations', []):
        add(edge['target_id'], edge['kind'], edge['reason'])
    # Current published direct children, siblings and parent are explicit syllabus
    # associations. Draft titles/parents never affect the relationship graph.
    parent = pub.snapshot.get('parent_id')
    for target in publications.values():
        if target.snapshot.get('parent_id') == pub.topic_id:
            add(target.topic_id, 'syllabus', 'A subtopic in this syllabus unit.')
    for target in publications.values():
        if parent is not None and target.snapshot.get('parent_id') == parent:
            add(target.topic_id, 'syllabus', 'In the same syllabus unit.')
    if parent: add(parent, 'syllabus', 'The parent syllabus unit.')
    return result[:6]


def article_links(pub, publications):
    from .connections import approved_links
    rows = approved_links(pub, publications)
    targets = {row['target_id'] for row in rows}
    cards = {pk: {**article_card(publications[pk], publications), 'description': description(publications[pk])} for pk in targets}
    return [{**row, 'target': cards[row['target_id']]} for row in rows]


def article_tags(pub):
    return list(pub.tags.filter(is_public=True).order_by('normalized_name').values('id', 'name', 'slug'))


def tag_page(slug, publications, page=1):
    tag = Tag.objects.filter(slug=slug, is_public=True).first()
    if tag is None: raise ServiceError('tag_unavailable', 'This tag is not available.', 404)
    ids = set(TopicPublication.objects.filter(tags=tag, is_published=True).values_list('topic_id', flat=True))
    rows = [p for pk, p in publications.items() if pk in ids and p.snapshot.get('blocks')]
    rows.sort(key=lambda p: (p.title.casefold(), p.topic_id))
    return {'tag': {'id': tag.pk, 'name': tag.name, 'slug': tag.slug}, 'count': len(rows), 'page': page, 'page_size': 30,
            'results': [article_card(p, publications) for p in rows[(page-1)*30:page*30]]}
