"""Canonical, read-only syllabus question collections. No question copying."""
from django.db.models import Q
from ..exceptions import ServiceError
from ..models import Topic, Question, Quiz
from .quiz import quiz_fingerprint, is_reviewable
from .publication import visible_publications


def subtree_ids(topic):
    rows = list(Topic.objects.values_list('pk', 'parent_id'))
    children = {}
    for pk, parent in rows:
        children.setdefault(parent, []).append(pk)
    found = set()
    pending = [topic.pk]
    for _ in range(32):
        if not pending:
            return found
        following = []
        for pk in pending:
            if pk in found:
                raise ServiceError('invalid_hierarchy', 'Syllabus hierarchy contains a cycle.')
            found.add(pk)
            following.extend(children.get(pk, []))
        pending = following
    raise ServiceError('invalid_hierarchy', 'Syllabus hierarchy is too deep.')


def question_collection(topic, *, reviewed_only=True):
    ids = subtree_ids(topic)
    rows = Question.objects.filter(Q(primary_topic_id__in=ids) | Q(related_topics__id__in=ids)).distinct().order_by('pk')
    if reviewed_only:
        visible = visible_publications()
        if topic.pk not in visible:
            return rows.none()
        quizzes = Quiz.objects.filter(topic_id__in=visible, review__is_approved=True).select_related('review').prefetch_related('questions__choices', 'questions__tags', 'questions__related_topics').order_by('pk')
        approved = [q.pk for q in quizzes if is_reviewable(q) and q.review.fingerprint == quiz_fingerprint(q)]
        # A hidden primary topic cannot be exposed through a related association.
        eligible = ids.intersection(visible)
        rows = rows.filter(Q(primary_topic_id__in=eligible) | Q(related_topics__id__in=eligible)).filter(primary_topic_id__in=visible, quiz_id__in=approved)
    return rows


def collection_questions(topic, publications):
    """One prefetched immutable-in-request graph for review, preview and grading."""
    if topic.pk not in publications:
        return []
    ids = subtree_ids(topic)
    ids = ids.intersection(publications)
    quizzes = Quiz.objects.filter(topic_id__in=publications, review__is_approved=True).filter(Q(questions__primary_topic_id__in=ids) | Q(questions__related_topics__id__in=ids)).distinct().select_related('review').prefetch_related('questions__choices', 'questions__tags', 'questions__related_topics').order_by('pk')
    result = {}
    for quiz in quizzes:
        if not is_reviewable(quiz) or quiz.review.fingerprint != quiz_fingerprint(quiz): continue
        for question in quiz.questions.all():
            if question.primary_topic_id in publications and (question.primary_topic_id in ids or any(t.pk in ids and t.pk in publications for t in question.related_topics.all())):
                result[question.pk] = (question, quiz.review.fingerprint)
    return [result[pk] for pk in sorted(result)]
