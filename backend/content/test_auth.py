from .test_helpers import publish_fixtures, review_fixtures
"""Student Authentication, User Ownership, and Cross-User Isolation Tests."""
from unittest.mock import patch
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import Bookmark, Choice, ContentBlock, Question, Quiz, QuizAttempt, Topic, UserProgress

if settings.TEST_RUNNER != "core.test_runner.NoMigrationRunner":
    raise RuntimeError("Use python run_tests.py: tests must not execute migrations")


class LearnerOwnershipTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.alice = User.objects.create_user(username="student-alice", password="alice-password-123", email="alice@test.local")
        cls.bob = User.objects.create_user(username="student-bob", password="bob-password-123", email="bob@test.local")
        cls.root = Topic.objects.create(title="Ancient Rajasthan", slug="ancient-rajasthan")
        cls.child = Topic.objects.create(title="Palaeolithic Era", slug="palaeolithic-era", parent=cls.root)
        ContentBlock.objects.create(topic=cls.root, block_type="text", content="<p>Historical evidence in Rajasthan.</p>", order=1)

        # Legacy ownerless records (user=None) to test preservation and isolation
        cls.legacy_bookmark = Bookmark.objects.create(topic=cls.root, user=None)
        cls.legacy_progress = UserProgress.objects.create(topic=cls.root, user=None, is_completed=True)
        cls.quiz = Quiz.objects.create(topic=cls.root, title="Rajasthan Prehistory Practice")
        cls.question = Question.objects.create(quiz=cls.quiz, question_text="What site has palaeolithic tools?", explanation="Bagor and Tilwara have evidence.")
        cls.choice = Choice.objects.create(question=cls.question, choice_text="Bagor", is_correct=True)
        Choice.objects.create(question=cls.question, choice_text="Unknown", is_correct=False)
        cls.legacy_attempt = QuizAttempt.objects.create(quiz=cls.quiz, score=1, total_questions=1, user=None)

    def setUp(self):
        publish_fixtures()
        review_fixtures()
        approval = override_settings(APPROVED_QUIZ_IDS=(self.quiz.pk,))
        approval.enable()
        self.addCleanup(approval.disable)

    def test_unauthenticated_requests_to_learner_endpoints_fail_cleanly(self):
        client = APIClient()
        # Learner actions require authentication
        self.assertEqual(client.post(f"/api/topic/{self.root.slug}/bookmark/").status_code, 401)
        self.assertEqual(client.post(f"/api/topic/{self.root.slug}/progress/").status_code, 401)
        self.assertEqual(client.get("/api/dashboard/").status_code, 401)
        self.assertEqual(client.get("/api/bookmarks/").status_code, 401)
        self.assertEqual(client.get("/api/progress/").status_code, 401)
        self.assertEqual(client.get("/api/profile/weaknesses/").status_code, 401)

    def test_guest_reading_remains_fully_functional_and_shows_unmarked_state(self):
        client = APIClient()
        # Syllabus tree loads without auth
        tree_res = client.get("/api/topics/?tree=1")
        self.assertEqual(tree_res.status_code, 200)
        nodes = tree_res.json()
        self.assertTrue(len(nodes) >= 1)
        # Topics show is_bookmarked=False and is_completed=False for guests
        for node in nodes:
            self.assertFalse(node["is_bookmarked"])
            self.assertFalse(node["is_completed"])

        # Topic detail loads without auth
        detail_res = client.get(f"/api/topic/{self.root.slug}/")
        self.assertEqual(detail_res.status_code, 200)
        self.assertFalse(detail_res.json()["is_bookmarked"])
        self.assertFalse(detail_res.json()["is_completed"])

    def test_student_registration_login_logout_and_status(self):
        client = APIClient()

        # Check initial unauthenticated status
        status = client.get("/api/auth/status/").json()
        self.assertFalse(status["authenticated"])
        self.assertIsNone(status["user"])

        # Registration with short password fails
        bad_reg = client.post("/api/auth/register/", {"username": "newstudent", "password": "123"})
        self.assertEqual(bad_reg.status_code, 400)

        # Successful registration
        reg = client.post("/api/auth/register/", {
            "username": "newstudent",
            "password": "valid-secure-password",
            "email": "newstudent@test.local",
            "name": "New Student",
        })
        self.assertEqual(reg.status_code, 200)
        data = reg.json()
        self.assertTrue(data["authenticated"])
        self.assertEqual(data["user"]["username"], "newstudent")
        self.assertEqual(data["user"]["name"], "New Student")

        # Status is now authenticated
        status = client.get("/api/auth/status/").json()
        self.assertTrue(status["authenticated"])
        self.assertEqual(status["user"]["username"], "newstudent")

        # Logout
        logout = client.post("/api/auth/logout/")
        self.assertEqual(logout.status_code, 200)
        self.assertFalse(logout.json()["authenticated"])

        # Status is now unauthenticated
        status = client.get("/api/auth/status/").json()
        self.assertFalse(status["authenticated"])

        # Login with bad credentials fails
        bad_login = client.post("/api/auth/login/", {"username": "newstudent", "password": "wrong"})
        self.assertEqual(bad_login.status_code, 401)

        # Login with valid credentials succeeds
        login = client.post("/api/auth/login/", {"username": "newstudent", "password": "valid-secure-password"})
        self.assertEqual(login.status_code, 200)
        self.assertTrue(login.json()["authenticated"])

    def test_bookmarks_are_user_scoped_with_no_cross_user_leakage(self):
        client_alice = APIClient()
        client_alice.force_login(self.alice)
        client_bob = APIClient()
        client_bob.force_login(self.bob)

        # Alice bookmarks root topic
        bm_res = client_alice.post(f"/api/topic/{self.root.slug}/bookmark/")
        self.assertEqual(bm_res.status_code, 200)
        self.assertTrue(bm_res.json()["is_bookmarked"])

        # Alice's topic detail shows is_bookmarked=True
        alice_detail = client_alice.get(f"/api/topic/{self.root.slug}/").json()
        self.assertTrue(alice_detail["is_bookmarked"])

        # Bob's topic detail shows is_bookmarked=False (complete isolation!)
        bob_detail = client_bob.get(f"/api/topic/{self.root.slug}/").json()
        self.assertFalse(bob_detail["is_bookmarked"])

        # Alice's dashboard has 1 bookmark
        alice_dash = client_alice.get("/api/dashboard/").json()
        self.assertEqual(len(alice_dash["bookmarks"]), 1)
        self.assertEqual(alice_dash["bookmarks"][0]["slug"], self.root.slug)

        # Bob's dashboard has 0 bookmarks
        bob_dash = client_bob.get("/api/dashboard/").json()
        self.assertEqual(len(bob_dash["bookmarks"]), 0)

        # Alice bookmarks list endpoint
        alice_bm = client_alice.get("/api/bookmarks/").json()
        self.assertEqual(len(alice_bm), 1)

        # Alice un-bookmarks topic
        toggle_res = client_alice.post(f"/api/topic/{self.root.slug}/bookmark/")
        self.assertEqual(toggle_res.status_code, 200)
        self.assertFalse(toggle_res.json()["is_bookmarked"])

        # Alice dashboard now has 0 bookmarks
        self.assertEqual(len(client_alice.get("/api/bookmarks/").json()), 0)

    def test_topic_completion_is_user_scoped(self):
        client_alice = APIClient()
        client_alice.force_login(self.alice)
        client_bob = APIClient()
        client_bob.force_login(self.bob)

        # Alice marks child topic as completed
        prog_res = client_alice.post(f"/api/topic/{self.child.slug}/progress/", {"is_completed": True}, format="json")
        self.assertEqual(prog_res.status_code, 200)
        self.assertTrue(prog_res.json()["is_completed"])

        # Alice topic detail shows is_completed=True
        self.assertTrue(client_alice.get(f"/api/topic/{self.child.slug}/").json()["is_completed"])

        # Bob topic detail shows is_completed=False
        self.assertFalse(client_bob.get(f"/api/topic/{self.child.slug}/").json()["is_completed"])

        # Alice dashboard reflects 1 completed topic
        alice_dash = client_alice.get("/api/dashboard/").json()
        self.assertEqual(alice_dash["stats"]["total_completed"], 1)
        self.assertEqual(len(alice_dash["completed_topics"]), 1)

        # Bob dashboard reflects 0 completed topics
        bob_dash = client_bob.get("/api/dashboard/").json()
        self.assertEqual(bob_dash["stats"]["total_completed"], 0)
        self.assertEqual(len(bob_dash["completed_topics"]), 0)

    def test_legacy_ownerless_records_remain_isolated_and_unaltered(self):
        # Verify that legacy records (user=None) exist and are never returned to Alice or Bob
        self.assertIsNone(self.legacy_bookmark.user)
        self.assertIsNone(self.legacy_progress.user)
        self.assertIsNone(self.legacy_attempt.user)

        client_alice = APIClient()
        client_alice.force_login(self.alice)
        dash = client_alice.get("/api/dashboard/").json()
        # Alice should see 0 bookmarks and 0 completed topics initially
        self.assertEqual(len(dash["bookmarks"]), 0)
        self.assertEqual(len(dash["completed_topics"]), 0)
        self.assertEqual(len(dash["quiz_attempts"]), 0)
