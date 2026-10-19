"""Read-only reviewed quiz selection and grading. Never persists learner state."""
import re
import hashlib
import json
from django.core import signing
from django.utils.crypto import salted_hmac
from django.db import transaction

from django.conf import settings
from django.db.models import Prefetch
from rest_framework import serializers

from ..models import Choice, Question, Quiz, QuizReview
from ..serializers import MAX_SAFE_ID, QuizSubmissionSerializer, is_valid_id


class QuizServiceError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message

    @property
    def payload(self):
        return {"error": {"code": self.code, "message": self.message}}


def unavailable():
    return QuizServiceError(404, "quiz_unavailable", "No reviewed quiz is available for this topic.")


def parse_quiz_id(value):
    """URL query IDs are canonical decimal strings; no numeric coercion surprises."""
    if (type(value) is not str or not value.isascii() or not value.isdecimal()
            or len(value) > 16 or value.startswith("0") or int(value) > MAX_SAFE_ID):
        raise QuizServiceError(400, "invalid_quiz_id", "Expected one positive integer quiz_id.")
    return int(value)


def approved_quiz_ids():
    """Comma-separated server setting; malformed configuration denies the whole list."""
    configured = getattr(settings, "APPROVED_QUIZ_IDS", ())
    if isinstance(configured, str):
        if not configured.strip():
            return ()
        try:
            configured = [parse_quiz_id(part.strip()) for part in configured.split(",")]
        except QuizServiceError:
            return ()
    if not isinstance(configured, (list, tuple, set, frozenset)):
        return ()
    if any(not is_valid_id(value) for value in configured):
        return ()
    return tuple(sorted(set(configured)))


def is_reviewable(quiz):
    """Minimum integrity checks do not replace the administrator's content review."""
    questions = list(quiz.questions.all())
    if not 1 <= len(questions) <= 100:
        return False
    for question in questions:
        text = " ".join(question.question_text.split()).casefold()
        if not text or re.fullmatch(r"which core aspect of .+ is key to rpsc preparation\?", text):
            return False  # Known auto-generated generic fallback, even if allowlisted.
        choices = list(question.choices.all())
        if (not 2 <= len(choices) <= 10 or any(not choice.choice_text.strip() for choice in choices)
                or sum(choice.is_correct for choice in choices) != 1):
            return False
    return True


def select_reviewed_quiz(slug, quiz_id=None, *, require_unambiguous=False):
    if quiz_id is not None and not is_valid_id(quiz_id):
        raise QuizServiceError(400, "invalid_quiz_id", "Expected one positive integer quiz_id.")
    quizzes = Quiz.objects.filter(topic__slug=slug, review__is_approved=True).order_by("pk")
    if quiz_id is not None:
        quizzes = quizzes.filter(pk=quiz_id)
    quizzes = quizzes.prefetch_related(Prefetch(
        "questions", queryset=Question.objects.order_by("pk").prefetch_related(
            Prefetch("choices", queryset=Choice.objects.order_by("pk"))
        ),
    ))
    candidates = [quiz for quiz in quizzes if is_reviewable(quiz) and QuizReview.objects.filter(quiz=quiz, is_approved=True, fingerprint=quiz_fingerprint(quiz)).exists()]
    if not candidates:
        raise unavailable()
    if require_unambiguous and quiz_id is None and len(candidates) > 1:
        raise QuizServiceError(409, "quiz_ambiguous", "Provide the quiz_id returned by quiz retrieval.")
    return candidates[0]


def grade_submission(slug, payload):
    """Validate everything before scoring. Internal only; no attempt creation.

    One point for each correct answer, zero for wrong/unanswered; no negative
    marking and no claim of official RPSC rules. Existing schema has no immutable
    question version: future owned attempts must add their own snapshot boundary.
    """
    serializer = QuizSubmissionSerializer(data=payload)
    try:
        serializer.is_valid(raise_exception=True)
    except serializers.ValidationError:
        raise QuizServiceError(400, "invalid_answers", "Invalid quiz submission format.") from None
    data = serializer.validated_data
    quiz = select_reviewed_quiz(slug, data.get("quiz_id"), require_unambiguous=True)
    return grade_quiz(quiz, data["answers"])


def grade_quiz(quiz, answers):
    questions = list(quiz.questions.all())
    by_id = {question.pk: question for question in questions}
    if len(answers) > len(questions) or set(answers) - by_id.keys():
        raise QuizServiceError(400, "invalid_answers", "Answers must belong to this quiz.")
    for question_id, choice_id in answers.items():
        if choice_id not in {choice.pk for choice in by_id[question_id].choices.all()}:
            raise QuizServiceError(400, "invalid_answers", "Each choice must belong to its question.")

    results = []
    for question in questions:
        choices = list(question.choices.all())
        correct = next(choice for choice in choices if choice.is_correct)
        selected = answers.get(question.pk)
        results.append({
            "question_id": question.pk,
            "question_text": question.question_text,
            "user_answer": selected,
            "correct_answer": correct.pk,
            "is_correct": selected == correct.pk,
            "explanation": question.explanation or "",
        })
    score = sum(result["is_correct"] for result in results)
    return {"quiz_id": quiz.pk, "score": score, "total": len(questions),
            "percentage": score * 100 / len(questions), "results": results}


def quiz_fingerprint(quiz):
    data = [quiz.pk, quiz.title, quiz.topic_id, [[q.pk, q.question_text, q.explanation,
        [[c.pk, c.choice_text, c.is_correct] for c in q.choices.all()]] for q in quiz.questions.all()]]
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def review_quiz(quiz, reviewer, source):
    # Fresh explicitly ordered instance; all callers use the same canonical order.
    quiz = Quiz.objects.prefetch_related(Prefetch("questions", queryset=Question.objects.order_by("pk").prefetch_related(Prefetch("choices", queryset=Choice.objects.order_by("pk"))))).get(pk=quiz.pk)
    if not source.strip() or not is_reviewable(quiz) or any(not q.explanation for q in quiz.questions.all()):
        raise QuizServiceError(400, "quiz_not_reviewable", "Review sources, explanations and one correct answer per question.")
    return QuizReview.objects.update_or_create(quiz=quiz, defaults={"is_approved": True, "fingerprint": quiz_fingerprint(quiz), "source_reference": source, "reviewed_by": reviewer})[0]


def revision_token(quiz):
    # Keyed opaque fingerprint prevents brute-forcing a plain answer-key digest.
    return signing.dumps({"quiz_id": quiz.pk, "revision": salted_hmac("quiz-revision", quiz_fingerprint(quiz)).hexdigest()}, salt="prepal-practice")


@transaction.atomic
def check_answers(slug, payload):
    if not isinstance(payload, dict) or set(payload) != {"quiz_id", "revision_token", "answers"} or not isinstance(payload.get("revision_token"), str) or len(payload['revision_token']) > 1000:
        raise QuizServiceError(400, "invalid_answers", "Provide quiz_id, revision_token and answers.")
    serializer = QuizSubmissionSerializer(data={k: payload[k] for k in ("quiz_id", "answers")})
    if not serializer.is_valid(): raise QuizServiceError(400, "invalid_answers", "Invalid answer format.")
    try:
        token = signing.loads(payload['revision_token'], salt="prepal-practice", max_age=3600)
    except signing.BadSignature:
        raise QuizServiceError(409, "quiz_changed", "Reload this practice set before checking answers.") from None
    quiz = select_reviewed_quiz(slug, serializer.validated_data['quiz_id'])
    expected = salted_hmac("quiz-revision", quiz_fingerprint(quiz)).hexdigest()
    if token != {"quiz_id": quiz.pk, "revision": expected}:
        raise QuizServiceError(409, "quiz_changed", "This practice set has changed. Reload it and try again.")
    return grade_quiz(quiz, serializer.validated_data['answers'])
