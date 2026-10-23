import re
from ..exceptions import ServiceError
from .publication import resolve_publication, plain


def terms(text):
    stop = {'the','and','for','with','from','this','that','what','which','who','how','why','when','where','does','did','are','was','were','can','could','would','should','tell','please','about','explain','lesson','topic','these','those','into','have','has','had','not','but','your'}
    return {s.casefold() for s in re.findall(r'\w+', text, re.UNICODE) if len(s) > 2 and s.casefold() not in stop}


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
        scope = [current]  # Non-expandable boundary, including direct/internal calls.
        evidence = []
        for pub in scope:
            for block in pub.snapshot.get('blocks', []):
                text = plain(block['content'])
                if block['block_type'] != 'text' or not text: continue
                evidence.append({'id': f'b{block["id"]}', 'topic_id': pub.topic_id, 'revision': pub.revision,
                    'title': pub.title, 'text': text, 'url': f'/topic/{pub.snapshot["slug"]}#{block["anchor"]}', 'kind': 'note'})
        selected = data.get('selected')
        if selected:
            source = next((e for e in evidence if e['id'] == selected['source_id'] and e['topic_id'] == current.topic_id), None)
            if not source or source['revision'] != selected['revision'] or plain(selected['text']) not in plain(source['text']):
                raise ServiceError('invalid_selection', 'Select text from the current published lesson.', 409)
        query = terms(data.get('message', ''))
        history_terms = terms(' '.join(m['text'] for m in data.get('history', [])[-2:]))
        followup = bool(query) and query <= {'more', 'mean', 'meaning', 'simple', 'simply', 'summary', 'summarize', 'again', 'simpler', 'detail', 'details'}
        for item in evidence:
            words = terms(item['text'])
            overlap = len(query & words)
            # History may rank relevant evidence, but cannot make an unrelated question relevant.
            item['score'] = 3 * overlap + (min(1, len(history_terms & words)) if overlap or followup else 0)
            if selected and selected['source_id'] == item['id']: item['score'] += 100
            if data.get('preset') and item['topic_id'] == current.topic_id: item['score'] += 1
        ranked = []
        for pub in scope:
            # Only current published note excerpts can become evidence.
            limit = 12
            ranked.extend(sorted((e for e in evidence if e['topic_id'] == pub.topic_id), key=lambda e: (-e['score'], e['id']))[:limit])
        selected_chunks = []; remaining = 18000
        for item in ranked:
            if item['score'] <= 0: continue
            text = item['text']
            if selected and item['id'] == selected['source_id']:
                at = plain(text).find(plain(selected['text'])); text = plain(text)[max(0, at - 300):at + len(selected['text']) + 1000]
            else:
                match = next((m for m in re.finditer(r'\w+', text, re.UNICODE) if m.group().casefold() in query), None)
                start = max(0, match.start() - 300) if match else 0
                text = text[start:start + 2400]
            text = text[:remaining]
            if not text: break
            selected_chunks.append({**item, 'text': text}); remaining -= len(text)
            if len(selected_chunks) >= 12: break
        return current, selected_chunks
