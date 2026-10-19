import json
import re
from django.conf import settings
from ..exceptions import ServiceError
from .publication import visible_publications
from .retrieval import DatabaseRetrievalProvider
from .providers import GeminiProvider, DemoProvider, SYSTEM
from .ai_budget import reserve, finish
from ..models import LearningResource


def answer(slug, data, visitor, ip_key):
    if not settings.AI_ENABLED or not settings.AI_GUEST_ENABLED or not settings.AI_MODEL or (not settings.DEMO_MODE and not settings.GEMINI_API_KEY):
        raise ServiceError('ai_unavailable', 'The tutor is temporarily unavailable. You can continue reading.', 503)
    current, evidence = DatabaseRetrievalProvider().retrieve(slug, data)
    if not current or not evidence:
        msg = 'Study notes for this syllabus topic are currently under editorial preparation. Grounded AI tutoring will be available as soon as verified notes and archival sources are published.' if not current else 'The published sources do not contain enough information to answer this. Try selecting a passage or asking about this lesson.'
        return {'response': msg, 'citations': [], 'status': 'insufficient_context', 'mocked': settings.DEMO_MODE}
    history = list(data.get('history', []))
    def bounded_prompt():
        return json.dumps({'question': data.get('message', ''), 'action': data.get('preset', ''), 'selection': data.get('selected'),
                           'history': history, 'evidence': evidence}, ensure_ascii=False)
    prompt = bounded_prompt()
    # UTF-8 bytes are a deliberately conservative tokenizer upper bound, plus framing margin.
    upper = len((SYSTEM + prompt).encode('utf-8')) + 512
    while upper > settings.AI_INPUT_TOKEN_LIMIT and (history or len(evidence) > 1):
        if history: history.pop(0)
        else: evidence.pop()
        prompt = bounded_prompt(); upper = len((SYSTEM + prompt).encode('utf-8')) + 512
    reservation = reserve(visitor, ip_key, upper)
    try:
        result, usage = (DemoProvider() if settings.DEMO_MODE else GeminiProvider()).generate(prompt, evidence)
    except Exception:
        finish(reservation)
        raise ServiceError('ai_unavailable', 'The tutor could not respond. Your learning materials remain available.', 503) from None
    actual = None
    if usage and type(usage.prompt_token_count) is int and type(usage.candidates_token_count) is int and not getattr(usage, 'thoughts_token_count', 0):
        actual = (usage.prompt_token_count * settings.AI_INPUT_RATE_MICRO + usage.candidates_token_count * settings.AI_OUTPUT_RATE_MICRO + 999999) // 1000000
    finish(reservation, 0 if settings.DEMO_MODE else actual)
    if (not isinstance(result, dict) or set(result) != {'answer', 'citations', 'insufficient'} or type(result['insufficient']) is not bool
            or not isinstance(result['answer'], str) or len(result['answer']) > 10000 or not isinstance(result['citations'], list)
            or any(type(c) is not str for c in result['citations']) or len(result['citations']) > 12):
        raise ServiceError('invalid_ai_response', 'The tutor returned an unsupported response. Please use the source material.', 502)
    if result['insufficient']:
        return {'response': 'The available sources do not support an answer to that question.', 'citations': [], 'status': 'insufficient_context', 'mocked': settings.DEMO_MODE}
    manifest = {e['id']: e for e in evidence}
    if not result['citations'] or any(c not in manifest for c in result['citations']) or re.search(r'https?://|\]\s*\(|<\s*[a-z!/]', result['answer'], re.I):
        raise ServiceError('invalid_citation', 'The tutor could not verify its references. Please use the source material.', 502)
    pubs = visible_publications(); citations = []
    for source_id in dict.fromkeys(result['citations']):
        source = manifest[source_id]; pub = pubs.get(source['topic_id'])
        if not pub or pub.revision != source['revision'] or (source['kind'] == 'pdf' and not LearningResource.objects.filter(pk=source['resource_id'], status='approved').exists()):
            raise ServiceError('source_changed', 'A source changed during this response. Reload the lesson.', 409)
        citations.append({k: source[k] for k in ['id', 'title', 'url', 'kind', 'revision']})
    return {'response': result['answer'], 'citations': citations, 'status': 'answered', 'mocked': settings.DEMO_MODE}
