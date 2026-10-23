"""Save reviewed practice results as immutable per-user snapshots, never question copies."""
from collections import defaultdict
import hashlib
import json
import uuid
from django.db import transaction, IntegrityError
from ..exceptions import ServiceError
from ..models import QuizAttempt, Question, Choice, Quiz, QuizReview, TopicPublication
from ..student_auth import rate_limit
from .publication import resolve_publication
from .quiz import check_answers, QuizServiceError
from .practice import check as check_collection
from .student import root_id


def result_of(attempt):
    return {**attempt.snapshot['result'], 'attempt_id': attempt.pk}


@transaction.atomic
def save_attempt(user, slug, data, collection=False):
    fields = {'collection_id','page','revision_token','answers','submission_id'} if collection else {'quiz_id','revision_token','answers','submission_id'}
    if type(data) is not dict or set(data) != fields or type(data.get('submission_id')) is not str or len(data['submission_id']) != 36:
        raise QuizServiceError(400,'invalid_answers','Provide the signed practice payload and a UUID submission_id.')
    try: submission_id=uuid.UUID(data['submission_id'])
    except ValueError: raise QuizServiceError(400,'invalid_answers','Provide a valid UUID submission_id.') from None
    digest=hashlib.sha256(json.dumps([slug,collection,data],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    existing=QuizAttempt.objects.filter(user=user,submission_id=submission_id).first()
    if existing:
        if existing.request_digest != digest: raise QuizServiceError(409,'submission_changed','Use a new submission ID for a different attempt.')
        return result_of(existing)
    rate_limit('practice-attempt',str(user.pk),200,86400)
    payload={k:v for k,v in data.items() if k!='submission_id'}
    checker=check_collection if collection else check_answers
    result=checker(slug,payload)
    ids=[r['question_id'] for r in result['results']]
    # Lock mutable canonical sources and revalidate the signed preview after acquiring locks.
    questions=list(Question.objects.filter(pk__in=ids).order_by('pk').select_for_update())
    list(Choice.objects.filter(question_id__in=ids).order_by('pk').select_for_update())
    quiz_ids=sorted({q.quiz_id for q in questions})
    list(Quiz.objects.filter(pk__in=quiz_ids).order_by('pk').select_for_update())
    list(QuizReview.objects.filter(quiz_id__in=quiz_ids).order_by('pk').select_for_update())
    source,pubs=resolve_publication(slug)
    relevant={source.topic_id, *(q.primary_topic_id for q in questions)}
    for pk in list(relevant):
        while pk in pubs and pubs[pk].snapshot.get('parent_id'):
            pk=pubs[pk].snapshot['parent_id']; relevant.add(pk)
    list(TopicPublication.objects.filter(topic_id__in=relevant).order_by('pk').select_for_update())
    result=checker(slug,payload)
    by_id={q.pk:q for q in Question.objects.filter(pk__in=ids).prefetch_related('choices')}
    entries=[]
    for row in result['results']:
        question=by_id[row['question_id']]; pub=pubs[question.primary_topic_id]
        root=root_id(question.primary_topic_id,pubs)
        entries.append({**row,'choices':[{'id':c.pk,'choice_text':c.choice_text} for c in sorted(question.choices.all(),key=lambda c:c.pk)],
            'topic_id':question.primary_topic_id,'topic_title':pub.title,'topic_slug':pub.snapshot['slug'],
            'subject_id':root,'subject_title':pubs[root].title if root in pubs else pub.title})
    snapshot={'version':1,'kind':'collection' if collection else 'quiz','title':source.title+' — practice',
        'source_topic_id':source.topic_id,'source_slug':source.snapshot['slug'],'source_revision':source.revision,
        'quiz_ids':quiz_ids,'questions':entries,'result':result}
    try:
        with transaction.atomic():
            attempt=QuizAttempt.objects.create(user=user,quiz_id=quiz_ids[0],collection_topic_id=source.topic_id if collection else None,
                submission_id=submission_id,snapshot=snapshot,request_digest=digest,score=result['score'],total_questions=result['total'])
            attempt.incorrect_questions.set([r['question_id'] for r in result['results'] if not r['is_correct']])
    except IntegrityError:
        attempt=QuizAttempt.objects.get(user=user,submission_id=submission_id)
        if attempt.request_digest!=digest: raise QuizServiceError(409,'submission_changed','Use a new submission ID for a different attempt.') from None
    return result_of(attempt)


def subject_performance(user):
    groups=defaultdict(lambda:{'correct':0,'total':0})
    for snapshot in QuizAttempt.objects.filter(user=user).values_list('snapshot',flat=True):
        for q in snapshot.get('questions',[]):
            key=(q['subject_id'],q['subject_title']); row=groups[key]
            row['total']+=1; row['correct']+=int(q['is_correct'])
    return [{'subject_id':pk,'title':title,**counts,'accuracy':round(100*counts['correct']/counts['total'],1)} for (pk,title),counts in groups.items()]
