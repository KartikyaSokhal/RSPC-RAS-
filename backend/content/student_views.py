"""Owned learner APIs; never adopt or expose legacy user=NULL records."""
from .permissions import student_endpoint
from .student_auth import require_student, reply
from .services.student import dashboard


@student_endpoint(['GET'])
def learner_dashboard(request):
    return reply(dashboard(require_student(request)))

from django.db import transaction
from django.utils import timezone
from .exceptions import ServiceError
from .models import Bookmark, UserProgress
from .student_auth import body, rate_limit
from .services.publication import resolve_publication, visible_publications
from .services.student import eligible_publications, card


def boolean_input(request, field):
    data = body(request, [field])
    if set(data) != {field} or type(data[field]) is not bool:
        raise ServiceError('invalid_request', f'{field} must be true or false.', 400)
    return data[field]


@student_endpoint(['GET'])
def user_bookmarks_list(request):
    user = require_student(request); pubs = visible_publications()
    rows = Bookmark.objects.filter(user=user, topic_id__in=pubs).order_by('-created_at', '-pk')
    return reply([{**card(pubs[row.topic_id]), 'bookmark_id': row.pk, 'created_at': row.created_at} for row in rows])


@student_endpoint(['GET'])
def user_progress_list(request):
    user = require_student(request); eligible = eligible_publications()
    rows = UserProgress.objects.filter(user=user, topic_id__in=eligible).order_by('-last_read_at')
    return reply([{**card(eligible[row.topic_id]), 'is_completed': row.is_completed,
                   'last_read_at': row.last_read_at, 'last_visited_at': row.last_visited_at} for row in rows])


@student_endpoint(['POST'])
def topic_bookmark(request, slug):
    user = require_student(request); requested = boolean_input(request, 'is_bookmarked')
    pub, _ = resolve_publication(slug)
    with transaction.atomic():
        if requested: Bookmark.objects.get_or_create(user=user, topic_id=pub.topic_id)
        else: Bookmark.objects.filter(user=user, topic_id=pub.topic_id).delete()
    return reply({'topic_id': pub.topic_id, 'is_bookmarked': requested})


@student_endpoint(['POST'])
def topic_progress(request, slug):
    user = require_student(request); requested = boolean_input(request, 'is_completed')
    pub, pubs = resolve_publication(slug)
    if pub.topic_id not in eligible_publications(pubs):
        raise ServiceError('not_learning_unit', 'Only published notes or approved PDF learning units can be completed.', 400)
    UserProgress.objects.update_or_create(user=user, topic_id=pub.topic_id, defaults={'is_completed': requested})
    return reply({'topic_id': pub.topic_id, 'is_completed': requested})


@student_endpoint(['POST'])
def topic_visit(request, slug):
    user = require_student(request); body(request, [])
    pub, pubs = resolve_publication(slug)
    if pub.topic_id not in eligible_publications(pubs):
        raise ServiceError('not_learning_unit', 'This syllabus outline has no published study material.', 400)
    rate_limit('visits', str(user.pk), 1000, 86400)
    UserProgress.objects.update_or_create(user=user, topic_id=pub.topic_id, defaults={'last_visited_at': timezone.now()})
    return reply({'topic_id': pub.topic_id, 'visited': True})

from .models import StudyPlan, StudyTask
from .services.planner import save_plan, plan_payload


@student_endpoint(['GET', 'POST'])
def study_plans(request):
    user = require_student(request)
    if request.method == 'POST':
        rate_limit('plan-create', str(user.pk), 30, 86400)
        return reply(plan_payload(save_plan(user, request.data)), 201)
    return reply([plan_payload(plan, include_tasks=False) for plan in StudyPlan.objects.filter(user=user).prefetch_related('tasks', 'selected_topics').order_by('-updated_at')])


@student_endpoint(['GET', 'POST'])
def study_plan(request, pk):
    user = require_student(request)
    plan = StudyPlan.objects.filter(pk=pk, user=user).first()
    if not plan: raise ServiceError('plan_not_found', 'Study plan not found.', 404)
    if request.method == 'POST': plan = save_plan(user, request.data, pk)
    return reply(plan_payload(plan))


@student_endpoint(['POST'])
def reschedule_plan(request, pk):
    user = require_student(request)
    data = body(request, ['revision', 'start_date'])
    plan = StudyPlan.objects.filter(pk=pk, user=user).first()
    if not plan: raise ServiceError('plan_not_found', 'Study plan not found.', 404)
    previous = plan_payload(plan, include_tasks=False)
    payload = {k: previous[k] for k in ('title', 'mode', 'study_days', 'daily_minutes', 'default_estimate_minutes', 'exam_date', 'topic_ids')}
    payload['exam_date'] = payload['exam_date'].isoformat() if payload['exam_date'] else None
    payload.update(start_date=data.get('start_date'), revision=data.get('revision'))
    return reply(plan_payload(save_plan(user, payload, pk)))


@student_endpoint(['POST'])
def study_task(request, pk, task_id):
    user = require_student(request); requested = boolean_input(request, 'is_completed')
    with transaction.atomic():
        plan = StudyPlan.objects.select_for_update().filter(pk=pk, user=user).first()
        if not plan: raise ServiceError('plan_not_found', 'Study plan not found.', 404)
        task = StudyTask.objects.filter(pk=task_id, plan=plan).first()
        if not task: raise ServiceError('task_not_found', 'Study task not found.', 404)
        if task.topic_id not in eligible_publications():
            raise ServiceError('topic_unavailable', 'This learning material is unavailable.', 409)
        if task.is_completed != requested:
            task.is_completed = requested; task.completed_at = timezone.now() if requested else None
            task.save(update_fields=['is_completed', 'completed_at'])
            plan.revision += 1; plan.save(update_fields=['revision', 'updated_at'])
    return reply(plan_payload(plan))

from .models import QuizAttempt
from .services.attempts import save_attempt
from .services.quiz import QuizServiceError


@student_endpoint(['POST'])
def topic_quiz_submit(request, slug):
    user=require_student(request)
    try:return reply(save_attempt(user,slug,request.data))
    except QuizServiceError as error:return reply(error.payload,error.status)


@student_endpoint(['POST'])
def practice_submit(request, slug):
    user=require_student(request)
    try:return reply(save_attempt(user,slug,request.data,collection=True))
    except QuizServiceError as error:return reply(error.payload,error.status)


@student_endpoint(['GET'])
def attempt_list(request):
    user=require_student(request)
    page=request.query_params.get('page','1')
    if len(page)>3 or not page.isascii() or not page.isdecimal() or not 1<=int(page)<=250:
        raise ServiceError('invalid_page','Choose a page from 1–250.',400)
    rows=QuizAttempt.objects.filter(user=user).select_related('quiz').order_by('-attempted_at','-pk')
    return reply({'count':rows.count(),'page':int(page),'results':[{'id':a.pk,'title':a.snapshot.get('title',a.quiz.title),'score':a.score,
        'total':a.total_questions,'attempted_at':a.attempted_at} for a in rows[(int(page)-1)*20:int(page)*20]]})


@student_endpoint(['GET'])
def attempt_detail(request, pk):
    user=require_student(request); row=QuizAttempt.objects.filter(user=user,pk=pk).first()
    if not row:raise ServiceError('attempt_not_found','Practice attempt not found.',404)
    return reply({'id':row.pk,'attempted_at':row.attempted_at,'score':row.score,'total':row.total_questions,'snapshot':row.snapshot,
        'history_available':bool(row.snapshot)})


@student_endpoint(['GET'])
def profile_weaknesses(request):
    user=require_student(request); counts={}
    rows=QuizAttempt.objects.filter(user=user)
    for snapshot in rows.values_list('snapshot',flat=True):
        for q in snapshot.get('questions',[]):
            if not q['is_correct']:
                key=q['topic_id']; counts.setdefault(key,{'topic_id':key,'title':q['topic_title'],'incorrect':0})['incorrect']+=1
    return reply({'weaknesses':list(counts.values()),'total_attempts':rows.count()})
