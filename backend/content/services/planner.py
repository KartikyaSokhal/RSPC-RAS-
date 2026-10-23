"""Deterministic, capacity-bounded schedules. No AI or external services."""
from collections import defaultdict
from datetime import date, timedelta
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from ..exceptions import ServiceError
from ..models import StudyPlan, StudyTask, Topic
from .publication import visible_publications
from .student import eligible_publications, ordered_units, root_id

FIELDS = {'title', 'mode', 'study_days', 'daily_minutes', 'default_estimate_minutes', 'start_date', 'exam_date', 'topic_ids'}


def bad(message):
    raise ServiceError('invalid_plan', message, 400)


def iso_date(value, label):
    try:
        if type(value) is not str or len(value) != 10: raise ValueError
        return date.fromisoformat(value)
    except (ValueError, TypeError): bad(f'Provide a valid {label} in YYYY-MM-DD format.')


def validate(data):
    if type(data) is not dict or set(data) != FIELDS: bad('Provide exactly the study-plan fields.')
    if type(data['title']) is not str or not 1 <= len(data['title'].strip()) <= 120: bad('Use a title of 1–120 characters.')
    if data['mode'] not in ('learn', 'revision'): bad('Choose learn or revision mode.')
    days = data['study_days']
    if (type(days) is not list or not 1 <= len(days) <= 7 or any(type(d) is not int or not 0 <= d <= 6 for d in days) or len(set(days)) != len(days)):
        bad('Choose distinct study days, Monday=0 through Sunday=6.')
    for field, low, high in [('daily_minutes', 15, 720), ('default_estimate_minutes', 15, 2400)]:
        if type(data[field]) is not int or not low <= data[field] <= high: bad(f'{field} must be an integer from {low} to {high}.')
    ids = data['topic_ids']
    if type(ids) is not list or not 1 <= len(ids) <= 250 or any(type(pk) is not int or pk <= 0 for pk in ids) or len(set(ids)) != len(ids):
        bad('Choose 1–250 distinct existing topic IDs.')
    start = iso_date(data['start_date'], 'start date')
    exam = iso_date(data['exam_date'], 'exam date') if data['exam_date'] is not None else None
    if exam and exam < start: bad('The exam target cannot precede the start date.')
    if not date(2000, 1, 1) <= start <= timezone.localdate() + timedelta(days=1827): bad('Choose a reasonable start date.')
    pubs = visible_publications(); eligible = eligible_publications(pubs)
    if any(pk not in pubs for pk in ids): bad('Selected subjects/topics must currently be published.')
    def included(pk):
        seen = set()
        while pk in pubs and pk not in seen:
            if pk in ids: return True
            seen.add(pk); pk = pubs[pk].snapshot.get('parent_id')
        return False
    selected = {pk: pub for pk, pub in eligible.items() if included(pk)}
    if not selected: bad('The selected branches have no published learning units.')
    return {k: data[k] for k in FIELDS - {'topic_ids', 'start_date', 'exam_date'}}, start, exam, ids, pubs, selected


def allocate(work, start, study_days, capacity):
    """Pure scheduling function: split stages to fit available study days exactly."""
    day = start; remaining = capacity; scheduled = []
    for topic_id, title, kind, minutes, used_default in work:
        while minutes:
            while day.weekday() not in study_days or remaining == 0:
                day += timedelta(days=1); remaining = capacity
                if (day - start).days > 730: bad('This plan exceeds two years. Increase study hours or reduce selected content.')
            size = min(minutes, remaining)
            scheduled.append({'topic_id': topic_id, 'topic_title': title, 'kind': kind,
                              'due_date': day, 'minutes': size, 'used_default': used_default})
            if len(scheduled) > 5000: bad('This plan has too many tasks. Reduce the selected content.')
            minutes -= size; remaining -= size
    return scheduled


def regenerate(plan, pubs, eligible, start):
    completed = defaultdict(int)
    for row in plan.tasks.filter(is_completed=True): completed[(row.topic_id, row.kind)] += row.minutes
    estimates = dict(Topic.objects.filter(pk__in=eligible).values_list('pk', 'estimated_study_minutes'))
    work = []
    for pk in ordered_units(pubs, eligible):
        estimate = estimates[pk] or plan.default_estimate_minutes
        if plan.mode == 'revision': estimate = max(15, (estimate + 1) // 2)
        # Total estimate includes learning, revision and practice; quick revision shifts the balance.
        learn = max(1, estimate * (60 if plan.mode == 'learn' else 20) // 100)
        revision = max(1, estimate * (20 if plan.mode == 'learn' else 50) // 100)
        stages = [('learn', learn), ('revision', revision), ('practice', estimate - learn - revision)]
        for kind, minutes in stages:
            remaining = max(0, minutes - completed[(pk, kind)])
            if remaining: work.append((pk, eligible[pk].title, kind, remaining, estimates[pk] is None))
    schedule = allocate(work, start, set(plan.study_days), plan.daily_minutes)
    # Only the current user's explicitly edited plan is changed. Completed IDs/timestamps survive.
    plan.tasks.filter(is_completed=False).delete()
    sequence = plan.tasks.aggregate(n=Max('sequence'))['n'] or 0
    StudyTask.objects.bulk_create([StudyTask(plan=plan, sequence=sequence+i+1, **row) for i, row in enumerate(schedule)])


@transaction.atomic
def save_plan(user, data, pk=None):
    if pk is not None:
        plan = StudyPlan.objects.select_for_update().filter(user=user, pk=pk).first()
        if not plan: raise ServiceError('plan_not_found', 'Study plan not found.', 404)
        if type(data) is not dict or type(data.get('revision')) is not int or data['revision'] != plan.revision:
            raise ServiceError('plan_changed', 'Reload the latest plan before editing.', 409)
        data = {k: v for k, v in data.items() if k != 'revision'}
    else:
        plan = StudyPlan(user=user)
    fields, start, exam, ids, pubs, eligible = validate(data)
    for key, value in fields.items(): setattr(plan, key, value.strip() if key == 'title' else value)
    plan.start_date, plan.exam_date = start, exam
    if pk: plan.revision += 1
    plan.save(); plan.selected_topics.set(ids)
    regenerate(plan, pubs, eligible, start)
    return plan


def plan_payload(plan, include_tasks=True):
    pubs = visible_publications(); eligible = eligible_publications(pubs)
    tasks = list(plan.tasks.all())
    week = defaultdict(lambda: {'minutes': 0, 'completed_minutes': 0, 'subjects': defaultdict(int)})
    month = defaultdict(lambda: {'minutes': 0, 'completed_minutes': 0, 'learning_units': 0, 'completed_units': 0})
    unit_tasks = defaultdict(list)
    for task in tasks:
        y, w, _ = task.due_date.isocalendar(); wk = week[f'{y}-W{w:02d}']; mo = month[task.due_date.strftime('%Y-%m')]
        for bucket in (wk, mo):
            bucket['minutes'] += task.minutes
            if task.is_completed: bucket['completed_minutes'] += task.minutes
        root = root_id(task.topic_id, pubs)
        if root in pubs: wk['subjects'][pubs[root].title] += task.minutes
        if task.topic_id in eligible: unit_tasks[task.topic_id].append(task)
    for rows in unit_tasks.values():
        target = month[max(t.due_date for t in rows).strftime('%Y-%m')]
        target['learning_units'] += 1
        target['completed_units'] += int(all(t.is_completed for t in rows))
    end = max((t.due_date for t in tasks), default=plan.start_date)
    total = sum(t.minutes for t in tasks); done = sum(t.minutes for t in tasks if t.is_completed)
    data = {'id': plan.pk, 'revision': plan.revision, 'title': plan.title, 'mode': plan.mode,
            'study_days': plan.study_days, 'daily_minutes': plan.daily_minutes,
            'default_estimate_minutes': plan.default_estimate_minutes, 'start_date': plan.start_date,
            'exam_date': plan.exam_date, 'topic_ids': list(plan.selected_topics.values_list('pk', flat=True)),
            'estimated_completion_date': end, 'exam_feasible': plan.exam_date is None or end <= plan.exam_date,
            'total_minutes': total, 'completed_minutes': done, 'progress_percentage': round(100*done/total, 1) if total else 0,
            'learning_unit_count': len({t.topic_id for t in tasks if t.topic_id in eligible}),
            'weekly_targets': [{'week': k, **v, 'subjects': dict(v['subjects'])} for k,v in sorted(week.items())],
            'monthly_targets': [{'month': k, **v} for k,v in sorted(month.items())],
            'estimates_are_approximate': True,
            'missing_estimate_topics': sorted({t.topic_id for t in tasks if t.used_default}),
            'unavailable_topic_ids': sorted({t.topic_id for t in tasks if t.topic_id not in eligible})}
    if include_tasks:
        data['tasks'] = [{'id': t.pk, 'topic_id': t.topic_id, 'title': t.topic_title,
            'slug': pubs[t.topic_id].snapshot['slug'] if t.topic_id in eligible else None,
            'kind': t.kind, 'due_date': t.due_date, 'minutes': t.minutes,
            'used_default': t.used_default, 'is_completed': t.is_completed, 'completed_at': t.completed_at} for t in tasks]
    return data
