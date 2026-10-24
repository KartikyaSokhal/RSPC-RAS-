"""Content-first release containment. All rows are synthetic isolated fixtures."""
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import connection
from django.test import TestCase, Client
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient

from .models import Bookmark, Choice, ContentBlock, Question, Quiz, QuizAttempt, Topic, UserProgress
from .services.publication import publish
from .services.quiz import review_quiz


class LearnerContainmentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.student = User.objects.create_user(username='student', password='fixture-password')
        cls.staff = User.objects.create_user(username='editor', password='fixture-password', is_staff=True)
        cls.admin = User.objects.create_superuser(username='administrator', password='fixture-password')
        cls.topic = Topic.objects.create(title='Synthetic lesson', slug='synthetic-lesson')
        cls.draft = Topic.objects.create(title='Draft outline', slug='draft-outline', parent=cls.topic)
        ContentBlock.objects.create(topic=cls.topic, block_type='text', content='<p>Reviewed fixture.</p>', source_reference='Synthetic fixture', order=1)
        publish(cls.topic, cls.admin)
        cls.quiz = Quiz.objects.create(topic=cls.topic, title='Synthetic quiz')
        cls.question = Question.objects.create(quiz=cls.quiz, question_text='Fixture?', explanation='Fixture explanation.')
        cls.correct = Choice.objects.create(question=cls.question, choice_text='Yes', is_correct=True)
        Choice.objects.create(question=cls.question, choice_text='No')
        review_quiz(cls.quiz, cls.admin, 'Synthetic fixture only')
        for owner in (None, cls.student, cls.staff, cls.admin):
            Bookmark.objects.create(topic=cls.topic, user=owner)
            UserProgress.objects.create(topic=cls.topic, user=owner, is_completed=True)
            attempt = QuizAttempt.objects.create(quiz=cls.quiz, user=owner, score=0, total_questions=1)
            attempt.incorrect_questions.add(cls.question)

    @property
    def blocked_urls(self):
        return ['/api/auth/register/', '/api/auth/login/', '/api/auth/logout/', '/api/auth/status/',
                '/api/dashboard/', '/api/bookmarks/', '/api/progress/', '/api/profile/weaknesses/',
                '/api/topic/synthetic-lesson/bookmark/', '/api/topic/synthetic-lesson/progress/',
                '/api/topic/synthetic-lesson/quiz/submit/']

    def snapshot(self):
        models = [get_user_model(), Session, Bookmark, UserProgress, QuizAttempt, QuizAttempt.incorrect_questions.through]
        return {model._meta.label: list(model.objects.order_by('pk').values_list()) for model in models}

    def test_every_identity_and_method_is_denied_without_queries_or_mutations(self):
        for actor in (None, self.student, self.staff, self.admin):
            client = APIClient(enforce_csrf_checks=True)
            if actor:
                client.force_login(actor)
            before = self.snapshot()
            with CaptureQueriesContext(connection) as queries:
                for url in self.blocked_urls + ['/api/topic/does-not-exist/bookmark/', '/api/topic/does-not-exist/quiz/submit/']:
                    for method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD'):
                        with self.subTest(actor=getattr(actor, 'username', 'guest'), url=url, method=method):
                            response = client.generic(method, url, data='malformed JSON', content_type='application/json', HTTP_AUTHORIZATION='Basic invalid')
                            self.assertEqual(response.status_code, 503)
                            self.assertEqual(response['Cache-Control'], 'no-store')
                            if method != 'HEAD':
                                self.assertEqual(response.json()['error']['code'], 'learner_features_unavailable')
            self.assertEqual(len(queries), 0)
            self.assertEqual(before, self.snapshot())

    def test_public_serializers_hide_even_owned_status_for_every_identity(self):
        for actor in (None, self.student, self.staff, self.admin):
            client = APIClient()
            if actor:
                client.force_login(actor)
            with CaptureQueriesContext(connection) as queries:
                for url in ('/api/topics/?tree=1', '/api/topics/?tree=1&published_only=1', '/api/topic/synthetic-lesson/', '/api/topic/draft-outline/'):
                    response = client.get(url)
                    self.assertEqual(response.status_code, 200)
                    def check(value):
                        if isinstance(value, dict):
                            for key, item in value.items():
                                if key in ('is_bookmarked', 'is_completed'):
                                    self.assertFalse(item)
                                else:
                                    check(item)
                        elif isinstance(value, list):
                            for item in value:
                                check(item)
                    check(response.json())
            self.assertFalse(any('content_bookmark' in q['sql'] or 'content_userprogress' in q['sql'] for q in queries))

    def test_stateless_grading_remains_available_without_learner_writes(self):
        for actor in (None, self.student, self.admin):
            client = APIClient(enforce_csrf_checks=True)
            if actor:
                client.force_login(actor)
            config = client.get('/api/config/').json()
            quiz = client.get('/api/topic/synthetic-lesson/quiz/').json()
            payload = {'quiz_id': quiz['id'], 'revision_token': quiz['revision_token'], 'answers': {str(self.question.pk): self.correct.pk}}
            before = self.snapshot()
            for _ in range(2):
                response = client.post('/api/topic/synthetic-lesson/quiz/check/', payload, format='json', HTTP_X_CSRFTOKEN=config['csrf_token'])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()['score'], 1)
                self.assertNotIn('attempt_id', response.json())
            self.assertEqual(before, self.snapshot())

    def test_admin_learner_records_reports_and_history_are_closed(self):
        for actor in (self.student, self.staff, self.admin):
            client = APIClient()
            client.force_login(actor)
            before = self.snapshot()
            urls = [f'/admin/auth/user/{self.student.pk}/report/', f'/admin/auth/user/{self.student.pk}/change/']
            for model in (Bookmark, UserProgress, QuizAttempt):
                base = f'/admin/content/{model._meta.model_name}/'
                urls.extend([base, base + 'add/', base + '1/change/', base + '1/delete/', base + '1/history/'])
            for url in urls:
                self.assertIn(client.get(url).status_code, (302, 403, 404))
                self.assertIn(client.post(url, {}).status_code, (302, 403, 404))
            self.assertEqual(before, self.snapshot())

    def test_admin_authentication_and_staff_account_management_still_work(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.get('/admin/login/').status_code, 200)
        response = client.post('/admin/login/', {'username': self.admin.username, 'password': 'fixture-password', 'csrfmiddlewaretoken': client.cookies['csrftoken'].value, 'next': '/admin/'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(client.get('/admin/').status_code, 200)
        users = client.get('/admin/auth/user/')
        self.assertEqual(users.status_code, 200)
        self.assertNotContains(users, '>student<')
        self.assertNotContains(users, 'Progress Report')
        self.assertEqual(client.get(f'/admin/auth/user/{self.staff.pk}/change/').status_code, 200)
        before = client.session.get('_auth_user_id')
        self.assertEqual(client.post('/api/auth/logout/').status_code, 503)
        self.assertEqual(client.session.get('_auth_user_id'), before)
        self.assertEqual(client.post('/admin/logout/', {'csrfmiddlewaretoken': client.cookies['csrftoken'].value}).status_code, 200)
        self.assertNotIn('_auth_user_id', client.session)
