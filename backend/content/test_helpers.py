"""Synthetic fixtures only; never imported by runtime code."""
from .models import Topic, ContentBlock, Quiz, Question
from .services.publication import publish
from .services.quiz import review_quiz, QuizServiceError


def publish_fixtures():
    ContentBlock.objects.filter(source_reference='').update(source_reference='Synthetic test fixture; not editorial content')
    pending = list(Topic.objects.all()); done = set()
    while pending:
        candidates = [t for t in pending if t.parent_id is None or t.parent_id in done]
        if not candidates: raise AssertionError('Fixture hierarchy cycle')
        for topic in candidates:
            publish(topic, None); done.add(topic.pk); pending.remove(topic)


def review_fixtures():
    Question.objects.filter(explanation__isnull=True).update(explanation='Synthetic explanation')
    Question.objects.filter(explanation='').update(explanation='Synthetic explanation')
    for quiz in Quiz.objects.all():
        try: review_quiz(quiz, None, 'Synthetic fixture source')
        except QuizServiceError: pass
