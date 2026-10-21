"""Dynamic collection manifests bind grading to the exact reviewed preview."""
import json
from django.core import signing
from django.db import transaction
from django.utils.crypto import salted_hmac
from ..exceptions import ServiceError
from ..serializers import QuizSubmissionSerializer, QuestionSerializer, is_valid_id
from .publication import resolve_publication
from .collections import collection_questions
from .quiz import grade_questions, QuizServiceError

PAGE_SIZE = 50
SALT = 'prepal-syllabus-practice'


def collection_state(slug, page):
    pub, publications = resolve_publication(slug)
    rows = collection_questions(pub.topic, publications)
    selected = rows[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
    questions = [q for q, _ in selected]
    if not questions: raise ServiceError('practice_unavailable', 'No reviewed questions are available in this collection.', 404)
    data = [pub.topic_id, page, [[q.pk, fingerprint, publications[q.primary_topic_id].revision] for q, fingerprint in selected]]
    digest = salted_hmac(SALT, json.dumps(data, separators=(',', ':'))).hexdigest()
    manifest = {'collection_id': pub.topic_id, 'page': page, 'digest': digest}
    return pub, questions, len(rows), manifest


def preview(slug, page):
    pub, questions, count, manifest = collection_state(slug, page)
    return {'id': pub.topic_id, 'collection_id': pub.topic_id, 'title': f'{pub.title} — syllabus practice', 'page': page,
            'count': count, 'page_size': PAGE_SIZE, 'questions': QuestionSerializer(questions, many=True).data,
            'revision_token': signing.dumps(manifest, salt=SALT)}


@transaction.atomic
def check(slug, payload):
    if (not isinstance(payload, dict) or set(payload) != {'collection_id', 'page', 'revision_token', 'answers'}
            or not is_valid_id(payload.get('collection_id')) or type(payload.get('page')) is not int
            or not 1 <= payload['page'] <= 250 or not isinstance(payload.get('revision_token'), str)
            or len(payload['revision_token']) > 1000):
        raise QuizServiceError(400, 'invalid_answers', 'Provide the collection ID, page, revision token and answers.')
    serializer = QuizSubmissionSerializer(data={'quiz_id': payload['collection_id'], 'answers': payload['answers']})
    if not serializer.is_valid(): raise QuizServiceError(400, 'invalid_answers', 'Invalid answer format.')
    try: manifest = signing.loads(payload['revision_token'], salt=SALT, max_age=3600)
    except signing.BadSignature: raise QuizServiceError(409, 'collection_changed', 'Reload this practice collection.') from None
    pub, questions, _, expected = collection_state(slug, payload['page'])
    if payload['collection_id'] != pub.topic_id or manifest != expected:
        raise QuizServiceError(409, 'collection_changed', 'This collection changed. Reload before checking answers.')
    return {'collection_id': pub.topic_id, **grade_questions(questions, serializer.validated_data['answers'])}
