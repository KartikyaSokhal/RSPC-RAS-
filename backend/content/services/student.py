"""Single counting rule: currently published content-bearing learning units.

A unit has nonempty published note text or a currently approved published PDF.
Structural headings/empty collections are excluded. Ancestor eligibility is the
existing publication resolver's responsibility. Drafts never enter this service.
"""
from django.conf import settings
from django.db.models import Sum
from ..models import Bookmark, UserProgress, QuizAttempt, Topic, LearningResource
from .publication import visible_publications, plain


def eligible_publications(pubs=None):
    pubs = visible_publications() if pubs is None else pubs
    resources = set(LearningResource.objects.filter(status='approved', topic_id__in=pubs).values_list('pk', flat=True))
    return {pk: pub for pk, pub in pubs.items() if any(
        b.get('block_type') == 'text' and plain(b.get('content', '')).strip() for b in pub.snapshot.get('blocks', [])
    ) or resources.intersection(pub.snapshot.get('resource_ids', []))}


def owned_status(user, pubs):
    if not settings.STUDENT_FEATURES_ENABLED or not user or not user.is_authenticated:
        return set(), set()
    bookmarks = set(Bookmark.objects.filter(user=user, topic_id__in=pubs).values_list('topic_id', flat=True))
    eligible = eligible_publications(pubs)
    completed = set(UserProgress.objects.filter(user=user, is_completed=True, topic_id__in=eligible).values_list('topic_id', flat=True))
    return bookmarks, completed


def card(pub):
    return {'id': pub.topic_id, 'topic_id': pub.topic_id, 'title': pub.title, 'slug': pub.snapshot['slug']}


def ordered_units(pubs, eligible):
    order = dict(Topic.objects.values_list('pk', 'order'))
    def key(pk):
        path = []; seen = set()
        while pk in pubs and pk not in seen:
            seen.add(pk); path.append((order.get(pk, 0), pk)); pk = pubs[pk].snapshot.get('parent_id')
        return tuple(reversed(path))
    return sorted(eligible, key=key)


def root_id(pk, pubs):
    seen = set()
    while pk in pubs and pk not in seen:
        seen.add(pk)
        parent = pubs[pk].snapshot.get('parent_id')
        if parent is None: return pk
        pk = parent
    return None


def dashboard(user):
    pubs = visible_publications(); eligible = eligible_publications(pubs)
    bookmarks, completed = owned_status(user, pubs)
    units = ordered_units(pubs, eligible)
    saved = Bookmark.objects.filter(user=user, topic_id__in=pubs).order_by('-created_at', '-pk')
    progress = UserProgress.objects.filter(user=user, topic_id__in=eligible)
    recent = list(progress.filter(last_visited_at__isnull=False).order_by('-last_visited_at', '-pk')[:10])
    suggested = [card(eligible[pk]) for pk in units if pk not in completed][:6]
    attempts = QuizAttempt.objects.filter(user=user)
    totals = attempts.aggregate(score=Sum('score'), total=Sum('total_questions'))
    subject_progress = []
    for pk, pub in pubs.items():
        if pub.snapshot.get('parent_id') is not None: continue
        ids = {i for i in eligible if root_id(i, pubs) == pk}
        done = len(ids & completed)
        subject_progress.append({**card(pub), 'total': len(ids), 'completed': done,
                                 'percentage': round(done * 100 / len(ids), 1) if ids else 0})
    from .attempts import subject_performance
    from .planner import plan_payload
    from ..models import StudyPlan
    plans = [plan_payload(plan, include_tasks=False) for plan in StudyPlan.objects.filter(user=user).prefetch_related('tasks', 'selected_topics').order_by('-updated_at')[:3]]
    return {
        'stats': {'total_topics': len(eligible), 'total_completed': len(completed),
            'progress_percentage': round(len(completed) * 100 / len(eligible), 1) if eligible else 0,
            'total_bookmarks': len(bookmarks), 'total_quizzes_taken': attempts.count(),
            'average_quiz_accuracy': round(totals['score'] * 100 / totals['total'], 1) if totals['total'] else None},
        'bookmarks': [{**card(pubs[b.topic_id]), 'bookmark_id': b.pk, 'created_at': b.created_at} for b in saved[:100]],
        'completed_topics': [{**card(eligible[p.topic_id]), 'last_read_at': p.last_read_at}
                             for p in progress.filter(is_completed=True).order_by('-last_read_at')[:100]],
        'recent_activity': [{**card(eligible[p.topic_id]), 'last_read_at': p.last_visited_at,
                             'is_completed': p.is_completed} for p in recent],
        'continue_studying': card(eligible[recent[0].topic_id]) if recent else (suggested[0] if suggested else None),
        'subject_progress': subject_progress, 'suggested_next': suggested,
        'subject_performance': subject_performance(user),
        'quiz_attempts': [{'id': a.pk, 'quiz_id': a.quiz_id, 'quiz_title': a.snapshot.get('title', a.quiz.title),
            'topic_title': pubs[a.quiz.topic_id].title if a.quiz.topic_id in pubs else 'Unavailable lesson',
            'topic_slug': a.snapshot.get('source_slug') if a.snapshot else (pubs[a.quiz.topic_id].snapshot['slug'] if a.quiz.topic_id in pubs else None),
            'score': a.score, 'total_questions': a.total_questions,
            'percentage': round(a.score * 100 / a.total_questions, 1) if a.total_questions else 0,
            'attempted_at': a.attempted_at} for a in attempts.select_related('quiz').order_by('-attempted_at', '-pk')[:20]],
        'study_plans': plans,
        'weekly_targets': plans[0]['weekly_targets'] if plans else [], 'monthly_targets': plans[0]['monthly_targets'] if plans else [],
        'counting_rule': 'Published units with readable notes or an approved attached PDF; structural headings are excluded.',
    }
