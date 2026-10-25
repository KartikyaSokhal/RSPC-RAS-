"""Public metadata, student-session boundary and staff isolation on SQLite/PG17."""
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, SimpleTestCase, override_settings
from rest_framework.test import APIClient
from core.public_demo_support import StudentLearningAccessMiddleware
from .models import Topic, ContentBlock, StudentIdentity, Bookmark, UserProgress, Quiz, Question, Choice, QuizAttempt
from .services.publication import publish
from .services.quiz import review_quiz
from .urls import urlpatterns


@override_settings(STUDENT_FEATURES_ENABLED=True, LEARNING_AUTH_REQUIRED=True,
                   STUDENT_REGISTRATION_ENABLED=False, PASSWORD_RESET_ENABLED=False,
                   AI_ENABLED=False, AI_GUEST_ENABLED=False,
                   MIDDLEWARE=[*settings.MIDDLEWARE, 'core.public_demo_support.StudentLearningAccessMiddleware'],
                   REST_FRAMEWORK={**settings.REST_FRAMEWORK, 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication']})
class PublicDemoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user('editor', password='Synthetic-Admin-423!', is_staff=True, is_superuser=True)
        cls.reader = User.objects.create_user('reader', password='Synthetic-Reader-423!', email='reader@example.invalid')
        cls.other = User.objects.create_user('other', password='Synthetic-Other-423!')
        cls.unbound = User.objects.create_user('unbound', password='Synthetic-Unbound-423!')
        for user in (cls.reader, cls.other):
            StudentIdentity.objects.create(user=user, email=user.username+'@example.invalid')
        cls.root = Topic.objects.create(title='Private subject title', slug='subject')
        cls.lesson = Topic.objects.create(title='Private lesson title', slug='lesson', parent=cls.root)
        ContentBlock.objects.create(topic=cls.lesson, block_type='text', order=1, content='<p>Private synthetic lesson notes.</p>', source_reference='Synthetic test fixture only')
        publish(cls.root, cls.staff); publish(cls.lesson, cls.staff)
        cls.quiz = Quiz.objects.create(topic=cls.lesson, title='Private quiz')
        cls.question = Question.objects.create(quiz=cls.quiz, primary_topic=cls.lesson, question_text='Private question?', explanation='Private explanation.')
        cls.correct = Choice.objects.create(question=cls.question, choice_text='Correct', is_correct=True)
        Choice.objects.create(question=cls.question, choice_text='Other')
        review_quiz(cls.quiz, cls.staff, 'Synthetic test only')

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

    def post(self, route, payload):
        csrf = self.client.get('/api/config/').json()['csrf_token']
        return self.client.post('/api/'+route, payload, format='json', HTTP_X_CSRFTOKEN=csrf)

    def test_every_nonpublic_api_fails_closed_for_guest_get_head_and_writes(self):
        for pattern in urlpatterns:
            path = '/api/'+str(pattern.pattern)
            for token in ('<slug:slug>', '<str:slug>'): path = path.replace(token, 'lesson')
            for token in ('<int:pk>', '<int:resource_id>', '<int:block_id>', '<int:task_id>'): path = path.replace(token, '1')
            if path in StudentLearningAccessMiddleware.PUBLIC: continue
            for method in ('GET', 'HEAD', 'POST', 'DELETE'):
                with self.subTest(path=path, method=method):
                    response = self.client.generic(method, path, data='{}', content_type='application/json')
                    self.assertEqual(response.status_code, 503 if path.startswith('/api/auth/') else 401)
                    self.assertNotIn('WWW-Authenticate', response)
                    self.assertNotIn(b'Private', response.content)
        self.assertFalse(Bookmark.objects.exists()); self.assertFalse(UserProgress.objects.exists()); self.assertFalse(QuizAttempt.objects.exists())
        self.assertEqual(self.client.get('/api/future-endpoint/').status_code, 401)

    def test_public_config_exposes_counts_policy_and_csrf_only_not_content(self):
        response = self.client.get('/api/config/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['public_summary'], {'subjects': 1, 'topics': 2})
        self.assertTrue(data['learning_auth_required']); self.assertFalse(data['registration_enabled'])
        self.assertFalse(data['ai_enabled']); self.assertFalse(data['password_reset_enabled'])
        self.assertNotIn('WWW-Authenticate', response)
        self.assertNotIn(b'Private', response.content)
        self.assertEqual(self.client.get('/api/health/').status_code, 200)

    def test_registration_is_closed_before_parsing_and_creates_no_users(self):
        count = get_user_model().objects.count()
        response = self.post('auth/register/', {'email': 'never-store@example.invalid'})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['error']['code'], 'registration_disabled')
        self.assertEqual(get_user_model().objects.count(), count)

    def test_csrf_session_persistence_login_read_and_logout(self):
        self.assertEqual(self.client.post('/api/auth/login/', {}, format='json').status_code, 403)
        response = self.post('auth/login/', {'username': 'reader', 'password': 'Synthetic-Reader-423!'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.cookies['sessionid']['httponly'])
        self.assertEqual(self.client.get('/api/topic/lesson/').status_code, 200)
        self.assertEqual(self.client.get('/api/topics/?tree=1').status_code, 200)
        self.assertEqual(self.client.get('/api/dashboard/').status_code, 200)
        self.assertTrue(self.client.get('/api/auth/status/').json()['authenticated'])
        self.assertEqual(self.client.post('/api/auth/logout/').status_code, 403)
        self.assertEqual(self.post('auth/logout/', {}).status_code, 200)
        self.assertEqual(self.client.get('/api/topic/lesson/').status_code, 401)

    def test_staff_unbound_and_inactive_users_do_not_get_student_access(self):
        for user in (self.staff, self.unbound):
            self.client.force_login(user)
            self.assertFalse(self.client.get('/api/auth/status/').json()['authenticated'])
            self.assertEqual(self.client.get('/api/topics/').status_code, 401)
        self.assertEqual(self.client.get('/admin/').status_code, 302)  # unbound student has no staff access
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get('/admin/').status_code, 200)
        self.assertEqual(self.client.post('/admin/content/topic/add/', {}).status_code, 403)
        self.client.logout()
        self.assertEqual(self.post('auth/login/', {'username': 'editor', 'password': 'Synthetic-Admin-423!'}).status_code, 401)
        self.reader.is_active = False; self.reader.save()
        self.assertEqual(self.post('auth/login/', {'username': 'reader', 'password': 'Synthetic-Reader-423!'}).status_code, 401)

    def test_basic_credentials_never_authenticate_or_challenge(self):
        response = self.client.get('/api/topics/', HTTP_AUTHORIZATION='Basic c3ludGhldGljOnVudXNlZA==')
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('WWW-Authenticate', response)
        self.assertEqual(self.client.get('/admin/').status_code, 302)

    def test_login_throttling_remains_enabled(self):
        for _ in range(8): self.assertEqual(self.post('auth/login/', {'username': 'reader', 'password': 'incorrect'}).status_code, 401)
        self.assertEqual(self.post('auth/login/', {'username': 'reader', 'password': 'incorrect'}).status_code, 429)

    def test_owned_bookmark_completion_and_attempt_isolation(self):
        import uuid
        self.client.force_login(self.reader)
        self.assertEqual(self.post('topic/lesson/bookmark/', {'is_bookmarked': True}).status_code, 200)
        self.assertEqual(self.post('topic/lesson/progress/', {'is_completed': True}).status_code, 200)
        preview = self.client.get('/api/topic/lesson/quiz/').json()
        saved = self.post('topic/lesson/quiz/submit/', {'quiz_id': preview['id'], 'revision_token': preview['revision_token'], 'answers': {str(self.question.pk): self.correct.pk}, 'submission_id': str(uuid.uuid4())})
        self.assertEqual(saved.status_code, 200, saved.json())
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f'/api/attempts/{saved.json()["attempt_id"]}/').status_code, 404)
        data = self.client.get('/api/topic/lesson/').json()
        self.assertFalse(data['is_bookmarked']); self.assertFalse(data['is_completed'])
        self.assertEqual(self.post('topic/lesson/bookmark/', {'is_bookmarked': True, 'user_id': self.reader.pk}).status_code, 400)
        self.assertEqual(Bookmark.objects.get().user_id, self.reader.pk)

    def test_signed_in_students_cannot_enable_external_services_or_registration(self):
        self.client.force_login(self.reader)
        self.assertEqual(self.post('auth/register/', {}).status_code, 503)
        self.assertEqual(self.post('auth/password-reset/', {}).status_code, 503)
        self.assertEqual(self.post('auth/google/start/', {}).status_code, 503)
        response = self.post('topic/lesson/chat/', {'message': 'Explain the lesson'})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['error']['code'], 'ai_unavailable')


class PublicDemoProfileTests(SimpleTestCase):
    def test_profile_refuses_hosted_unmarked_sqlite_and_production_targets(self):
        with TemporaryDirectory() as root:
            marker = Path(root)/'.public-demo.json'
            marker.write_text(json.dumps({'kind': 'prepal-local-public-demo-v1', 'state': 'ready', 'database': 'prepal_local_public_demo_test'}))
            env = {**os.environ, 'PYTHON_DOTENV_DISABLED': '1', 'PREPAL_PUBLIC_DEMO': '1', 'PREPAL_LOCAL_POSTGRES': '1', 'PREPAL_DEMO_ROOT': root, 'DATABASE_ENGINE': 'postgresql', 'POSTGRES_HOST': '127.0.0.1', 'POSTGRES_DB': 'prepal_local_public_demo_test', 'POSTGRES_USER': 'synthetic', 'POSTGRES_PASSWORD': 'unused-synthetic', 'DJANGO_ENV': 'development'}
            command = [sys.executable, '-c', 'import core.public_demo_settings']
            for changes in ({}, {'RENDER': 'true'}, {'POSTGRES_HOST': 'unexpected.example'}, {'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': ':memory:'}, {'DJANGO_ENV': 'production'}, {'PREPAL_PUBLIC_DEMO': ''}, {'POSTGRES_DB': 'prepal_staging_db'}, {'PREPAL_DEMO_ROOT': root+'/missing'}):
                result = subprocess.run(command, cwd=Path(__file__).resolve().parents[1], env={**env, **changes}, capture_output=True)
                self.assertEqual(result.returncode == 0, not bool(changes), str(changes))
