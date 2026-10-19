from .test_helpers import publish_fixtures, review_fixtures
from .models import QuizReview
from .services.quiz import review_quiz
"""P003 read-only retrieval and deterministic grading on disposable fixture tables."""
from unittest.mock import patch
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient
from .models import Bookmark, Choice, ContentBlock, Question, Quiz, QuizAttempt, Topic, UserProgress
from .services.quiz import QuizServiceError, approved_quiz_ids, grade_submission

if settings.TEST_RUNNER != "core.test_runner.NoMigrationRunner":
    raise RuntimeError("Use python run_tests.py: tests must not execute migrations")


class QuizSafetyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.topic = Topic.objects.create(title="Reviewed fixture topic", slug="reviewed-fixture")
        cls.other = Topic.objects.create(title="Other fixture", slug="other-fixture")
        cls.empty_topic = Topic.objects.create(title="No quiz", slug="no-quiz")
        cls.quiz = Quiz.objects.create(topic=cls.topic, title="Reviewed fixture")
        cls.first = Question.objects.create(quiz=cls.quiz, question_text="First question?", explanation="Fixture explanation")
        cls.correct = Choice.objects.create(question=cls.first, choice_text="Right", is_correct=True)
        cls.wrong = Choice.objects.create(question=cls.first, choice_text="Wrong")
        cls.second = Question.objects.create(quiz=cls.quiz, question_text="Second question?")
        cls.second_correct = Choice.objects.create(question=cls.second, choice_text="Right 2", is_correct=True)
        Choice.objects.create(question=cls.second, choice_text="Wrong 2")
        cls.other_quiz = Quiz.objects.create(topic=cls.other, title="Other reviewed fixture")
        cls.foreign_question = Question.objects.create(quiz=cls.other_quiz, question_text="Other question?")
        cls.foreign_choice = Choice.objects.create(question=cls.foreign_question, choice_text="Other right", is_correct=True)
        Choice.objects.create(question=cls.foreign_question, choice_text="Other wrong")
        cls.attempt = QuizAttempt.objects.create(quiz=cls.quiz, score=0, total_questions=2)
        cls.attempt.incorrect_questions.add(cls.first)
        Bookmark.objects.create(topic=cls.topic)
        UserProgress.objects.create(topic=cls.topic, is_completed=True)

    def setUp(self):
        publish_fixtures()
        review_fixtures()
        approval = override_settings(APPROVED_QUIZ_IDS=(self.quiz.pk, self.other_quiz.pk))
        approval.enable()
        self.addCleanup(approval.disable)
        self.url = f"/api/topic/{self.topic.slug}/quiz/"

    def snapshot(self):
        models = [Topic, ContentBlock, Quiz, Question, Choice, QuizAttempt,
                  QuizAttempt.incorrect_questions.through, Bookmark, UserProgress]
        return {model._meta.label: list(model.objects.order_by("pk").values_list()) for model in models}

    def payload(self, answers=None, **extra):
        return {"quiz_id": self.quiz.pk, "answers": answers if answers is not None else {str(self.first.pk): self.correct.pk}, **extra}

    def assert_error(self, payload, status=400, code="invalid_answers"):
        with self.assertRaises(QuizServiceError) as raised:
            grade_submission(self.topic.slug, payload)
        self.assertEqual((raised.exception.status, raised.exception.code), (status, code))

    def new_quiz(self):
        quiz = Quiz.objects.create(topic=self.topic, title="Another reviewed fixture")
        q = Question.objects.create(quiz=quiz, question_text="Additional question?")
        c = Choice.objects.create(question=q, choice_text="Correct additional", is_correct=True)
        Choice.objects.create(question=q, choice_text="Wrong additional")
        q.explanation = "Synthetic explanation"; q.save()
        review_quiz(quiz, None, "Synthetic source")
        return quiz, q, c

    @patch("content.ai_engine.generate_quiz_questions")
    @patch("content.ai_engine.generate_mentor_response")
    def test_repeated_get_is_read_only_ordered_and_never_calls_ai(self, mentor, generate):
        before = self.snapshot()
        bodies = []
        with CaptureQueriesContext(connection) as queries:
            for _ in range(3):
                response = self.client.get(self.url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["Cache-Control"], "no-store")
                bodies.append(response.json())
        self.assertTrue(all(q["sql"].lstrip().upper().startswith("SELECT") for q in queries))
        self.assertEqual(bodies, [bodies[0]] * 3)
        self.assertEqual(bodies[0]["id"], self.quiz.pk)
        self.assertEqual([q["id"] for q in bodies[0]["questions"]], [self.first.pk, self.second.pk])
        self.assertEqual([c["id"] for c in bodies[0]["questions"][0]["choices"]], [self.correct.pk, self.wrong.pk])
        self.assertEqual(set(bodies[0]), {"id", "title", "time_limit_seconds", "questions", "revision_token"})
        self.assertEqual(set(bodies[0]["questions"][0]), {"id", "question_text", "choices"})
        self.assertEqual(set(bodies[0]["questions"][0]["choices"][0]), {"id", "choice_text"})
        self.assertEqual(before, self.snapshot())
        generate.assert_not_called()
        mentor.assert_not_called()

    @patch("content.ai_engine.generate_quiz_questions")
    def test_missing_quiz_and_unknown_topic_return_404_without_creating_or_generating(self, generate):
        before = self.snapshot()
        for slug in [self.empty_topic.slug, "not-a-topic"]:
            for _ in range(2):
                response = self.client.get(f"/api/topic/{slug}/quiz/")
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.json()["error"]["code"], "quiz_unavailable")
        self.assertEqual(before, self.snapshot())
        generate.assert_not_called()

    def test_empty_and_malformed_allowlists_fail_closed(self):
        for config in [(), "", None, True, 1, {}, "1,invalid", "1,", "01", "1.0", [True], [1.0], ["1"], [-1], [2**53]]:
            with self.subTest(config=config), override_settings(APPROVED_QUIZ_IDS=config):
                self.assertEqual(approved_quiz_ids(), ())
                # Legacy allowlist parsing stays fail-closed; persisted review is now required.
                QuizReview.objects.all().delete()
                response = self.client.get(self.url)
                self.assertEqual(response.status_code, 404)

    def test_comma_separated_allowlist_is_explicit_and_sorted(self):
        with override_settings(APPROVED_QUIZ_IDS=f" {self.other_quiz.pk}, {self.quiz.pk},{self.quiz.pk} "):
            self.assertEqual(approved_quiz_ids(), tuple(sorted([self.quiz.pk, self.other_quiz.pk])))
            self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_unapproved_foreign_and_unknown_quiz_ids_never_fall_back(self):
        unapproved, _, _ = self.new_quiz()
        QuizReview.objects.filter(quiz=unapproved).update(is_approved=False)
        for quiz_id in [unapproved.pk, self.other_quiz.pk, 900000]:
            response = self.client.get(self.url, {"quiz_id": quiz_id})
            self.assertEqual(response.status_code, 404)
            self.assert_error(self.payload(quiz_id=quiz_id), 404, "quiz_unavailable")

    def test_malformed_query_ids_are_predictable_400(self):
        for query in ["quiz_id=", "quiz_id=true", "quiz_id=1.0", "quiz_id=-1", "quiz_id=01",
                      "quiz_id=1&quiz_id=2", "quiz_id=" + "9" * 5000, "quiz_id=9007199254740992"]:
            with self.subTest(query=query[:45]):
                response = self.client.get(self.url + "?" + query)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()["error"]["code"], "invalid_quiz_id")

    def test_multiple_quizzes_have_stable_retrieval_and_explicit_grading_identity(self):
        newer, question, correct = self.new_quiz()
        with override_settings(APPROVED_QUIZ_IDS=(newer.pk, self.quiz.pk)):
            self.assertEqual(self.client.get(self.url).json()["id"], self.quiz.pk)
            selected = self.client.get(self.url, {"quiz_id": newer.pk}).json()
            self.assertEqual(selected["id"], newer.pk)
            result = grade_submission(self.topic.slug, {"quiz_id": selected["id"], "answers": {str(question.pk): correct.pk}})
            self.assertEqual((result["quiz_id"], result["score"], result["total"]), (newer.pk, 1, 1))
            self.assert_error({"answers": {}}, 409, "quiz_ambiguous")
            self.assertEqual(grade_submission(self.topic.slug, self.payload())["quiz_id"], self.quiz.pk)

    def test_single_quiz_legacy_input_resolves_same_id(self):
        result = grade_submission(self.topic.slug, {"answers": {str(self.first.pk): self.correct.pk}})
        self.assertEqual(result["quiz_id"], self.client.get(self.url).json()["id"])

    def test_known_fallback_is_rejected_even_when_allowlisted(self):
        for text in ["Which core aspect of 'Fixture' is key to RPSC preparation?",
                     "  WHICH  CORE ASPECT OF 'Fixture' IS KEY TO RPSC PREPARATION? "]:
            self.first.question_text = text
            self.first.save()  # Synthetic fixture only.
            before = self.snapshot()
            self.assertEqual(self.client.get(self.url).status_code, 404)
            self.assert_error(self.payload(), 404, "quiz_unavailable")
            self.assertEqual(before, self.snapshot())

    def test_empty_quiz_is_unavailable_not_a_zero_question_success(self):
        empty = Quiz.objects.create(topic=self.topic, title="Empty fixture")
        QuizReview.objects.all().update(is_approved=False)
        with override_settings(APPROVED_QUIZ_IDS=(empty.pk,)):
            self.assertEqual(self.client.get(self.url).status_code, 404)
            self.assert_error(self.payload(quiz_id=empty.pk), 404, "quiz_unavailable")

    def test_invalid_question_scoring_rules_reject_entire_quiz(self):
        for wrong_correct, right_correct in [(False, False), (True, True)]:
            Choice.objects.filter(pk=self.correct.pk).update(is_correct=right_correct)
            Choice.objects.filter(pk=self.wrong.pk).update(is_correct=wrong_correct)
            self.assertEqual(self.client.get(self.url).status_code, 404)
            self.assert_error(self.payload(), 404, "quiz_unavailable")

    def test_blank_question_or_choice_and_single_choice_fail_closed(self):
        for model, key, field in [(Question, self.first.pk, "question_text"), (Choice, self.wrong.pk, "choice_text")]:
            old = getattr(model.objects.get(pk=key), field)
            model.objects.filter(pk=key).update(**{field: "  "})
            self.assertEqual(self.client.get(self.url).status_code, 404)
            model.objects.filter(pk=key).update(**{field: old})
        self.wrong.delete()  # Disposable fixture only.
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_malformed_payloads_rejected_before_database_access(self):
        for payload in [None, [], "text", 1, True, {}, {"answers": None}, {"answers": []},
                        {"answers": "text"}, {"answers": {}, "user_id": 1}, {"answers": {}, "unexpected": 1}]:
            with self.subTest(payload=payload), self.assertNumQueries(0):
                self.assert_error(payload)

    def test_strict_quiz_choice_and_question_id_types(self):
        for value in [True, False, 0, -1, 1.0, "1", None, [], {}, 2**53]:
            with self.subTest(quiz_id=value), self.assertNumQueries(0):
                self.assert_error(self.payload(quiz_id=value))
            with self.subTest(choice_id=value), self.assertNumQueries(0):
                self.assert_error(self.payload({str(self.first.pk): value}))
        for key in ["", "01", "0", "-1", "+1", "1.0", " 1", "١", "9" * 5000, "9007199254740992", 1]:
            with self.subTest(question_key=str(key)[:30]), self.assertNumQueries(0):
                self.assert_error(self.payload({key: self.correct.pk}))

    def test_foreign_questions_cross_question_choices_and_excess_answers_rejected(self):
        before = self.snapshot()
        for answers in [{str(self.foreign_question.pk): self.foreign_choice.pk},
                        {str(self.first.pk): self.second_correct.pk},
                        {str(self.first.pk): self.foreign_choice.pk},
                        {str(self.first.pk): 900000},
                        {str(self.first.pk): self.correct.pk, str(self.second.pk): self.second_correct.pk, "900000": self.correct.pk}]:
            self.assert_error(self.payload(answers))
        self.assertEqual(before, self.snapshot())

    def test_deterministic_score_handles_correct_wrong_and_unanswered_without_writes(self):
        before = self.snapshot()
        cases = [({}, 0), ({str(self.first.pk): self.correct.pk}, 1),
                 ({str(self.first.pk): self.wrong.pk, str(self.second.pk): self.second_correct.pk}, 1),
                 ({str(self.first.pk): self.correct.pk, str(self.second.pk): self.second_correct.pk}, 2)]
        with CaptureQueriesContext(connection) as queries:
            for answers, score in cases:
                result = grade_submission(self.topic.slug, self.payload(answers))
                self.assertEqual((result["score"], result["total"], result["percentage"]), (score, 2, score * 50))
                self.assertEqual(result, grade_submission(self.topic.slug, self.payload(dict(reversed(list(answers.items()))))))
                self.assertEqual([row['question_id'] for row in result['results']], [self.first.pk, self.second.pk])
                if not answers:
                    self.assertTrue(all(row['user_answer'] is None for row in result['results']))
        self.assertTrue(all(q["sql"].lstrip().upper().startswith("SELECT") for q in queries))
        self.assertEqual(before, self.snapshot())

    def test_revoked_approval_denies_preview_and_grading(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        QuizReview.objects.all().update(is_approved=False)
        with override_settings(APPROVED_QUIZ_IDS=()):
            self.assertEqual(self.client.get(self.url).status_code, 404)
            self.assert_error(self.payload(), 404, "quiz_unavailable")

    def test_submissions_require_authentication_and_enforce_user_ownership(self):
        User = get_user_model()
        alice = User.objects.create_user(username="quiz-alice")
        bob = User.objects.create_user(username="quiz-bob")

        # Unauthenticated request returns 401
        client = APIClient()
        response = client.post(self.url + "submit/", self.payload(), format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "auth_required")

        # Authenticated Alice can submit valid practice set
        client_alice = APIClient()
        client_alice.force_login(alice)
        from content.services.quiz import revision_token
        payload = {**self.payload(), "revision_token": revision_token(self.quiz)}
        res_alice = client_alice.post(self.url + "submit/", payload, format="json")
        self.assertEqual(res_alice.status_code, 200)
        self.assertEqual(res_alice.json()["score"], 1)
        self.assertIn("attempt_id", res_alice.json())


        # Verify attempt has user=alice, NOT bob or ownerless
        attempt = QuizAttempt.objects.get(pk=res_alice.json()["attempt_id"])
        self.assertEqual(attempt.user, alice)
        self.assertEqual(QuizAttempt.objects.filter(user=bob).count(), 0)

