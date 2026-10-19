import re
from ..models import ResourcePage, LearningResource
from ..exceptions import ServiceError
from .publication import resolve_publication, plain


def terms(text):
    return {s.casefold() for s in re.findall(r'\w+', text, re.UNICODE) if len(s) > 2}


class DatabaseRetrievalProvider:
    def retrieve(self, slug, data):
        try:
            current, pubs = resolve_publication(slug)
        except ServiceError:
            from ..models import Topic
            topic = Topic.objects.filter(slug=slug).first()
            if not topic:
                raise ServiceError('topic_not_found', 'This lesson is not available.', 404)
            return None, []
        scope = [current]
        if data.get('allow_related'):
            for relation in current.snapshot.get('relations', []):
                pub = pubs.get(relation['target_id'])
                if pub and pub.topic_id not in {p.topic_id for p in scope}: scope.append(pub)
                if len(scope) >= 3: break
        evidence = []
        for pub in scope:
            for block in pub.snapshot.get('blocks', []):
                text = plain(block['content'])
                if block['block_type'] != 'text' or not text: continue
                evidence.append({'id': f'b{block["id"]}', 'topic_id': pub.topic_id, 'revision': pub.revision,
                    'title': pub.title, 'text': text, 'url': f'/topic/{pub.snapshot["slug"]}#{block["anchor"]}', 'kind': 'note'})
            resource_ids = list(LearningResource.objects.filter(pk__in=pub.snapshot.get('resource_ids', []), topic_id=pub.topic_id, status='approved').values_list('pk', flat=True))
            for page in ResourcePage.objects.filter(resource_id__in=resource_ids).select_related('resource').order_by('resource_id', 'page_number')[:400]:
                evidence.append({'id': f'r{page.resource_id}p{page.page_number}', 'topic_id': pub.topic_id, 'revision': pub.revision,
                    'title': f'{page.resource.title} · page {page.page_number}', 'text': page.text,
                    'url': f'/resources/{page.resource_id}?page={page.page_number}', 'kind': 'pdf', 'resource_id': page.resource_id, 'page': page.page_number})
        selected = data.get('selected')
        if selected:
            source = next((e for e in evidence if e['id'] == selected['source_id'] and e['topic_id'] == current.topic_id), None)
            if not source or source['revision'] != selected['revision'] or plain(selected['text']) not in plain(source['text']):
                raise ServiceError('invalid_selection', 'Select text from the current published lesson.', 409)
        query = terms(data.get('message', ''))
        history_terms = terms(' '.join(m['text'] for m in data.get('history', [])[-2:]))
        for item in evidence:
            words = terms(item['text'])
            item['score'] = 3 * len(query & words) + min(1, len(history_terms & words))
            if selected and selected['source_id'] == item['id']: item['score'] += 100
            if data.get('preset') and item['topic_id'] == current.topic_id: item['score'] += 1
        ranked = []
        for pub in scope:
            # Keep room for explicitly permitted related evidence instead of filling all slots with current notes.
            limit = 8 if pub == current and len(scope) > 1 else 12 if pub == current else 2
            ranked.extend(sorted((e for e in evidence if e['topic_id'] == pub.topic_id), key=lambda e: (-e['score'], e['id']))[:limit])
        selected_chunks = []; remaining = 18000
        for item in ranked:
            if item['score'] <= 0: continue
            text = item['text']
            if selected and item['id'] == selected['source_id']:
                at = plain(text).find(plain(selected['text'])); text = plain(text)[max(0, at - 300):at + len(selected['text']) + 1000]
            else: text = text[:2400]
            text = text[:remaining]
            if not text: break
            selected_chunks.append({**item, 'text': text}); remaining -= len(text)
            if len(selected_chunks) >= 12: break
        return current, selected_chunks
