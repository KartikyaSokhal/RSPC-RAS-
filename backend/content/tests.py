from .test_helpers import publish_fixtures, review_fixtures
"""Existing-behavior regression baseline, not certification of known flaws."""
from unittest.mock import patch

from django.conf import settings
from django.db import connection
from django.test import TestCase, override_settings

from .ai_engine import get_topic_context
from .models import Choice, ContentBlock, Question, Quiz, QuizAttempt, Topic

if settings.TEST_RUNNER != "core.test_runner.NoMigrationRunner":
    raise RuntimeError("Use python run_tests.py: this baseline must not execute migrations")


class BaselineAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = Topic.objects.create(title="Fixture History", slug="fixture-history", order=2)
        cls.first = Topic.objects.create(title="Fixture Geography", slug="fixture-geography", order=1)
        cls.child = Topic.objects.create(title="Child", slug="fixture-child", parent=cls.root, order=1)
        ContentBlock.objects.create(topic=cls.root, block_type="text", content="Fixture notes.", order=2)
        ContentBlock.objects.create(topic=cls.root, block_type="heading", content="Fixture heading", order=1)
        cls.quiz = Quiz.objects.create(topic=cls.root, title="Fixture quiz", time_limit_seconds=180)
        cls.question = Question.objects.create(quiz=cls.quiz, question_text="Fixture question?", explanation="Fixture explanation.")
        cls.correct = Choice.objects.create(question=cls.question, choice_text="Correct", is_correct=True)
        Choice.objects.create(question=cls.question, choice_text="Wrong")

    def setUp(self):
        publish_fixtures()
        review_fixtures()
        approval = override_settings(APPROVED_QUIZ_IDS=(self.quiz.pk,))
        approval.enable()
        self.addCleanup(approval.disable)

    def test_database_is_in_memory_without_migration_history(self):
        self.assertEqual(connection.settings_dict["NAME"], ":memory:")
        self.assertNotIn("django_migrations", connection.introspection.table_names())

    def test_roots_are_ordered_and_exclude_children(self):
        response = self.client.get("/api/topics/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([t["slug"] for t in response.json()], [self.first.slug, self.root.slug])
        self.assertTrue(response.json()[1]["has_children"])

    def test_detail_preserves_block_order_and_child_links(self):
        response = self.client.get(f"/api/topic/{self.root.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([b["block_type"] for b in response.json()["blocks"]], ["heading", "text"])
        self.assertEqual(response.json()["children"][0]["slug"], self.child.slug)

    def test_catalog_reads_do_not_change_content_counts(self):
        before = (Topic.objects.count(), ContentBlock.objects.count(), Quiz.objects.count())
        self.client.get("/api/topics/")
        self.client.get(f"/api/topic/{self.root.slug}/")
        self.assertEqual(before, (Topic.objects.count(), ContentBlock.objects.count(), Quiz.objects.count()))

    def test_unknown_topic_returns_404(self):
        self.assertEqual(self.client.get("/api/topic/missing-fixture/").status_code, 404)

    def test_admin_requires_login(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_empty_chat_is_rejected_without_provider(self):
        response = self.client.post(f"/api/topic/{self.root.slug}/chat/", {}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_chat_is_default_off_without_paid_authorization(self):
        response = self.client.post(f"/api/topic/{self.root.slug}/chat/", {"message": "Explain this"}, content_type="application/json")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["error"]["code"], "ai_unavailable")

    @patch("content.ai_engine.generate_quiz_questions")
    def test_existing_quiz_does_not_generate_or_disclose_correctness(self, generate):
        response = self.client.get(f"/api/topic/{self.root.slug}/quiz/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.quiz.id)
        self.assertEqual(set(response.json()["questions"][0]["choices"][0]), {"id", "choice_text"})
        generate.assert_not_called()
        self.assertEqual(Quiz.objects.count(), 1)

    def test_quiz_submission_requires_authentication_without_saving(self):
        response = self.client.post(f"/api/topic/{self.root.slug}/quiz/submit/", {
            "answers": {str(self.question.id): self.correct.id},
        }, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "auth_required")
        self.assertEqual(QuizAttempt.objects.count(), 0)

    def test_unanswered_submission_cannot_create_an_ownerless_attempt(self):
        response = self.client.post(f"/api/topic/{self.root.slug}/quiz/submit/", {"answers": {}}, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(QuizAttempt.objects.count(), 0)


    def test_context_contains_current_notes_not_unrelated_content(self):
        ContentBlock.objects.create(topic=self.first, block_type="text", content="Unrelated fixture", order=1)
        context = get_topic_context(self.root)
        self.assertIn("Fixture notes.", context)
        self.assertNotIn("Unrelated fixture", context)

    def test_empty_parent_does_not_infer_unapproved_child_scope(self):
        ContentBlock.objects.create(topic=self.child, block_type="text", content="Child fixture notes", order=1)
        self.root.blocks.all().delete()  # Ephemeral synthetic rows only.
        self.assertNotIn("Child fixture notes", get_topic_context(self.root))
