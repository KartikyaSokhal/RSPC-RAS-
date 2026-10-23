"""Owned student platform regressions; isolated data and mocked external providers."""
import time
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient
from .models import AuthRateWindow, StudentIdentity


@override_settings(STUDENT_FEATURES_ENABLED=False)
class StudentClosedGateTests(TestCase):
    def test_new_routes_are_query_free_and_fail_closed_for_guest_and_staff(self):
        staff = get_user_model().objects.create_superuser(username='gate-staff', password='synthetic')
        guest = APIClient(enforce_csrf_checks=True)
        signed = APIClient(enforce_csrf_checks=True); signed.force_login(staff)
        routes = ['account/deletion/', 'auth/password-reset/', 'auth/password-reset/confirm/', 'auth/google/start/', 'auth/google/callback/',
                  'plans/', 'plans/1/', 'plans/1/reschedule/', 'plans/1/tasks/1/', 'attempts/', 'attempts/1/',
                  'topic/not-published/visit/', 'topic/not-published/practice/submit/']
        for client in (guest, signed):
            for route in routes:
                for method in ('GET', 'POST', 'DELETE'):
                    with self.subTest(route=route, method=method), self.assertNumQueries(0):
                        response = client.generic(method, '/api/' + route, data='not-json', content_type='application/json')
                        self.assertEqual(response.status_code, 503)
                        self.assertEqual(response.json()['error']['code'], 'learner_features_unavailable')


@override_settings(STUDENT_FEATURES_ENABLED=True)
class StudentAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.password = 'Synthetic-Learning-423!'

    def post(self, path, data, client=None):
        client = client or self.client
        csrf = client.get('/api/config/').json()['csrf_token']
        return client.post('/api/' + path, data, format='json', HTTP_X_CSRFTOKEN=csrf)

    def register(self, **changes):
        return self.post('auth/register/', {'username': 'reader', 'email': 'reader@example.test', 'password': self.password, **changes})

    def test_registration_session_login_logout_and_email_login(self):
        response = self.register()
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get()
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertEqual(StudentIdentity.objects.get().user_id, user.pk)
        self.assertTrue(self.client.get('/api/auth/status/').json()['authenticated'])
        self.assertEqual(self.client.cookies['sessionid']['httponly'], True)
        self.assertEqual(self.post('auth/logout/', {}).status_code, 200)
        self.assertFalse(self.client.get('/api/auth/status/').json()['authenticated'])
        self.assertEqual(self.post('auth/login/', {'username': 'READER@example.test', 'password': self.password}).status_code, 200)

    def test_csrf_required_for_guest_register_login_and_authenticated_logout(self):
        self.assertEqual(self.client.post('/api/auth/register/', {}, format='json').status_code, 403)
        self.assertEqual(self.client.post('/api/auth/login/', {}, format='json').status_code, 403)
        self.register()
        self.assertEqual(self.client.post('/api/auth/logout/').status_code, 403)

    def test_duplicate_normalized_accounts_weak_password_and_malformed_input(self):
        self.assertEqual(self.register().status_code, 200)
        for changes in ({'username': 'READER', 'email': 'new@example.test'}, {'username': 'second', 'email': 'READER@example.test'}):
            self.assertEqual(self.register(**changes).status_code, 409)
        self.assertEqual(self.register(username='another', email='other@example.test', password='12345678').status_code, 400)
        self.assertEqual(self.post('auth/login/', {'username': [], 'password': self.password}).status_code, 400)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_password_reset_email_single_use_and_session_invalidation(self):
        self.register()
        before = self.client.session.session_key
        self.assertEqual(self.post('auth/password-reset/', {'email': 'reader@example.test'}).status_code, 202)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/reset-password#uid=', mail.outbox[0].body)
        user = get_user_model().objects.get()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        payload = {'uid': uid, 'token': token, 'password': 'Different-Synthetic-524!'}
        self.assertEqual(self.post('auth/password-reset/confirm/', payload).status_code, 200)
        self.assertEqual(self.post('auth/password-reset/confirm/', payload).status_code, 400)
        self.assertFalse(self.client.get('/api/auth/status/').json()['authenticated'])
        self.assertNotEqual(before, self.client.session.session_key)
        self.assertEqual(self.post('auth/password-reset/', {'email': 'missing@example.test'}).status_code, 202)

    def test_login_rate_limit_and_no_plaintext_identifiers_in_limiter(self):
        for _ in range(8):
            self.assertEqual(self.post('auth/login/', {'username': 'missing', 'password': self.password}).status_code, 401)
        self.assertEqual(self.post('auth/login/', {'username': 'missing', 'password': self.password}).status_code, 429)
        self.assertTrue(all(len(key) == 64 and 'missing' not in key for key in AuthRateWindow.objects.values_list('key', flat=True)))

    @override_settings(SITE_ORIGIN='')
    def test_recovery_configuration_errors_do_not_disclose_account_presence(self):
        self.register()
        known = self.post('auth/password-reset/', {'email': 'reader@example.test'})
        unknown = self.post('auth/password-reset/', {'email': 'missing@example.test'})
        self.assertEqual(known.status_code, 503)
        self.assertEqual(known.json(), unknown.json())

    @override_settings(GOOGLE_CLIENT_ID='synthetic-client', GOOGLE_CLIENT_SECRET='synthetic-client-fixture', GOOGLE_REDIRECT_URI='http://127.0.0.1:8000/api/auth/google/callback/')
    def test_google_adapter_verifies_signed_token_with_configured_audience(self):
        from .student_auth import exchange_google
        with patch('requests.post') as send, patch('google.oauth2.id_token.verify_oauth2_token', return_value={'sub': 'synthetic'}) as verify:
            send.return_value.json.return_value = {'id_token': 'synthetic-signed-fixture'}
            self.assertEqual(exchange_google('synthetic-code', 'synthetic-verifier'), {'sub': 'synthetic'})
            self.assertEqual(send.call_args.kwargs['timeout'], 10)
            self.assertEqual(send.call_args.kwargs['data']['code_verifier'], 'synthetic-verifier')
            self.assertEqual(verify.call_args.args[2], 'synthetic-client')

    def test_google_unconfigured_is_clear_and_no_network(self):
        with patch('content.student_auth.exchange_google') as exchange:
            self.assertEqual(self.post('auth/google/start/', {}).status_code, 503)
            exchange.assert_not_called()

    @override_settings(GOOGLE_CLIENT_ID='synthetic-client', GOOGLE_CLIENT_SECRET='synthetic-client-fixture', GOOGLE_REDIRECT_URI='http://127.0.0.1:8000/api/auth/google/callback/')
    def test_google_state_nonce_audience_issuer_verified_email_and_replay(self):
        def start():
            response = self.post('auth/google/start/', {})
            self.assertEqual(response.status_code, 200)
            self.assertIn('code_challenge_method=S256', response.json()['url'])
            return self.client.session['google_auth']
        state = start()
        claims = {'iss': 'https://accounts.google.com', 'aud': 'synthetic-client', 'sub': 'provider-123', 'email': 'google@example.test', 'email_verified': True, 'nonce': state['nonce'], 'exp': time.time() + 100}
        with patch('content.student_auth.exchange_google', return_value=claims):
            self.assertEqual(self.client.get('/api/auth/google/callback/', {'state': 'wrong', 'code': 'fixture'}).status_code, 400)
        for update in ({'nonce': 'wrong'}, {'aud': 'other'}, {'iss': 'https://attacker.test'}, {'email_verified': False}, {'exp': 1}):
            state = start()
            with patch('content.student_auth.exchange_google', return_value={**claims, 'nonce': state['nonce'], **update}):
                self.assertEqual(self.client.get('/api/auth/google/callback/', {'state': state['state'], 'code': 'fixture'}).status_code, 400)
        state = start()
        with patch('content.student_auth.exchange_google', return_value={**claims, 'nonce': state['nonce']}):
            self.assertEqual(self.client.get('/api/auth/google/callback/', {'state': state['state'], 'code': 'fixture'}).status_code, 302)
            self.assertEqual(self.client.get('/api/auth/google/callback/', {'state': state['state'], 'code': 'fixture'}).status_code, 400)
        identity = StudentIdentity.objects.get()
        self.assertEqual(identity.google_subject, 'provider-123')
        self.assertFalse(identity.user.has_usable_password())
        self.assertNotIn('id_token', self.client.session)

    @override_settings(GOOGLE_CLIENT_ID='synthetic-client', GOOGLE_CLIENT_SECRET='synthetic-client-fixture', GOOGLE_REDIRECT_URI='http://127.0.0.1:8000/api/auth/google/callback/')
    def test_google_never_implicitly_links_existing_password_or_staff_account(self):
        self.register()
        self.post('auth/logout/', {})
        self.post('auth/google/start/', {})
        state = self.client.session['google_auth']
        claims = {'iss': 'accounts.google.com', 'aud': 'synthetic-client', 'sub': 'another-sub', 'email': 'reader@example.test', 'email_verified': True, 'nonce': state['nonce'], 'exp': time.time()+100}
        with patch('content.student_auth.exchange_google', return_value=claims):
            self.assertEqual(self.client.get('/api/auth/google/callback/', {'state': state['state'], 'code': 'fixture'}).status_code, 409)
        self.assertIsNone(StudentIdentity.objects.get().google_subject)

from django.utils import timezone
from .models import Topic, ContentBlock, TopicPublication, Bookmark, UserProgress, Quiz, QuizAttempt
from .services.publication import publish


@override_settings(STUDENT_FEATURES_ENABLED=True)
class StudentDashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.editor = User.objects.create_superuser(username='editor', password='synthetic')
        cls.reader = User.objects.create_user(username='reader', password='synthetic')
        cls.other = User.objects.create_user(username='other', password='synthetic')
        cls.root = Topic.objects.create(title='Subject', slug='subject')
        publish(cls.root, cls.editor)
        cls.lessons = []
        for i in range(3):
            topic = Topic.objects.create(title=f'Lesson {i}', slug=f'lesson-{i}', parent=cls.root, order=i)
            ContentBlock.objects.create(topic=topic, block_type='text', content=f'<p>Published content {i}.</p>', source_reference='Synthetic fixture', order=1)
            publish(topic, cls.editor); cls.lessons.append(topic)
        cls.quiz = Quiz.objects.create(topic=cls.lessons[0], title='Reviewed practice fixture')

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.client.force_login(self.reader)

    def test_empty_dashboard_uses_published_learning_units_not_hardcoded_or_structural_nodes(self):
        data = self.client.get('/api/dashboard/').json()
        self.assertEqual(data['stats']['total_topics'], 3)
        self.assertEqual(data['stats']['total_completed'], 0)
        self.assertIsNone(data['stats']['average_quiz_accuracy'])
        self.assertEqual(data['continue_studying']['id'], self.lessons[0].pk)
        self.assertEqual(data['subject_progress'][0]['total'], 3)

    def test_guests_denied_and_ownerless_other_user_records_never_counted(self):
        Bookmark.objects.create(topic=self.lessons[0])
        Bookmark.objects.create(user=self.other, topic=self.lessons[0])
        UserProgress.objects.create(user=self.other, topic=self.lessons[0], is_completed=True)
        UserProgress.objects.create(topic=self.lessons[0], is_completed=True)
        QuizAttempt.objects.create(user=self.other, quiz=self.quiz, score=1, total_questions=1)
        self.assertEqual(self.client.get('/api/dashboard/').json()['stats']['total_bookmarks'], 0)
        self.assertEqual(self.client.get('/api/dashboard/').json()['stats']['total_completed'], 0)
        self.assertEqual(self.client.get('/api/dashboard/').json()['stats']['total_quizzes_taken'], 0)
        self.client.logout(); self.assertEqual(self.client.get('/api/dashboard/').status_code, 401)

    def test_withdrawn_units_never_count_in_progress_and_continue_uses_actual_visit(self):
        for topic in self.lessons:
            UserProgress.objects.create(user=self.reader, topic=topic, is_completed=True)
        UserProgress.objects.filter(user=self.reader, topic=self.lessons[1]).update(last_visited_at=timezone.now())
        TopicPublication.objects.filter(topic=self.lessons[2]).update(is_published=False)
        data = self.client.get('/api/dashboard/').json()
        self.assertEqual(data['stats']['total_topics'], 2)
        self.assertEqual(data['stats']['total_completed'], 2)
        self.assertEqual(data['stats']['progress_percentage'], 100)
        self.assertEqual(data['continue_studying']['id'], self.lessons[1].pk)
        self.assertEqual(len(data['recent_activity']), 1)

    def test_attempt_counts_and_accuracy_use_all_records_not_recent_twenty(self):
        for _ in range(25): QuizAttempt.objects.create(user=self.reader, quiz=self.quiz, score=1, total_questions=2)
        data = self.client.get('/api/dashboard/').json()
        self.assertEqual(data['stats']['total_quizzes_taken'], 25)
        self.assertEqual(data['stats']['average_quiz_accuracy'], 50)
        self.assertEqual(len(data['quiz_attempts']), 20)


class OwnedTopicStateTests(StudentDashboardTests):
    def post(self, path, data, client=None):
        client = client or self.client
        csrf = client.get('/api/config/').json()['csrf_token']
        return client.post('/api/' + path, data, format='json', HTTP_X_CSRFTOKEN=csrf)

    def test_bookmarks_completion_idempotence_isolation_and_ownerless_preservation(self):
        lesson = self.lessons[0]
        legacy = Bookmark.objects.create(topic=lesson)
        other = UserProgress.objects.create(user=self.other, topic=lesson, is_completed=True)
        for _ in range(2):
            self.assertEqual(self.post('topic/lesson-0/bookmark/', {'is_bookmarked': True}).status_code, 200)
            self.assertEqual(self.post('topic/lesson-0/progress/', {'is_completed': True}).status_code, 200)
        self.assertEqual(Bookmark.objects.filter(user=self.reader).count(), 1)
        self.assertEqual(UserProgress.objects.filter(user=self.reader).count(), 1)
        data = self.client.get('/api/topic/lesson-0/').json()
        self.assertTrue(data['is_bookmarked']); self.assertTrue(data['is_completed'])
        self.assertEqual(self.post('topic/lesson-0/bookmark/', {'is_bookmarked': False}).status_code, 200)
        self.assertEqual(self.post('topic/lesson-0/progress/', {'is_completed': False}).status_code, 200)
        self.assertTrue(Bookmark.objects.filter(pk=legacy.pk).exists())
        other.refresh_from_db(); self.assertTrue(other.is_completed)
        self.assertEqual(self.client.get('/api/dashboard/').json()['stats']['total_completed'], 0)

    def test_rejected_draft_guest_cross_user_invalid_boolean_and_csrf_writes(self):
        TopicPublication.objects.filter(topic=self.lessons[1]).update(is_published=False)
        self.assertEqual(self.post('topic/lesson-1/bookmark/', {'is_bookmarked': True}).status_code, 404)
        for payload in ({'is_completed': 'false'}, {'is_completed': 1}, {'is_completed': True, 'user_id': self.other.pk}, {}):
            self.assertEqual(self.post('topic/lesson-0/progress/', payload).status_code, 400)
        self.assertEqual(self.client.post('/api/topic/lesson-0/progress/', {'is_completed': True}, format='json').status_code, 403)
        self.assertEqual(self.post('topic/subject/progress/', {'is_completed': True}).status_code, 400)
        self.client.logout()
        self.assertEqual(self.post('topic/lesson-0/bookmark/', {'is_bookmarked': True}).status_code, 401)
        self.assertFalse(UserProgress.objects.exists()); self.assertFalse(Bookmark.objects.exists())

    def test_visits_require_explicit_post_and_never_mark_completion(self):
        for _ in range(2): self.client.get('/api/topic/lesson-0/')
        self.assertFalse(UserProgress.objects.exists())
        self.assertEqual(self.post('topic/lesson-0/visit/', {}).status_code, 200)
        row = UserProgress.objects.get(user=self.reader)
        self.assertFalse(row.is_completed); self.assertIsNotNone(row.last_visited_at)
        self.assertEqual(self.client.get('/api/dashboard/').json()['continue_studying']['id'], self.lessons[0].pk)

from datetime import date
from .models import StudyPlan, StudyTask
from .services.planner import allocate


class StudyPlannerTests(OwnedTopicStateTests):
    def payload(self, **changes):
        return {'title': 'My fixture plan', 'mode': 'learn', 'study_days': [0,2,4],
                'daily_minutes': 60, 'default_estimate_minutes': 90, 'start_date': '2026-10-26',
                'exam_date': None, 'topic_ids': [self.root.pk], **changes}

    def test_pure_schedule_respects_weekdays_capacity_and_preserves_all_minutes(self):
        work = [(1, 'Fixture lesson', 'learn', 130, False)]
        rows = allocate(work, date(2026,10,26), {0,2}, 60)
        self.assertEqual([r['due_date'].isoformat() for r in rows], ['2026-10-26','2026-10-28','2026-11-02'])
        self.assertEqual([r['minutes'] for r in rows], [60,60,10])

    def test_defaults_editor_estimates_modes_feasibility_and_subject_aggregation(self):
        self.lessons[0].estimated_study_minutes = 120; self.lessons[0].save()
        data = self.post('plans/', self.payload(exam_date='2026-10-26')).json()
        self.assertEqual(data['total_minutes'], 300)
        self.assertEqual(data['missing_estimate_topics'], [self.lessons[1].pk, self.lessons[2].pk])
        self.assertFalse(data['exam_feasible'])
        self.assertTrue(data['weekly_targets'][0]['subjects'])
        self.assertEqual(sum(m['learning_units'] for m in data['monthly_targets']), 3)
        self.assertEqual(sum(m['completed_units'] for m in data['monthly_targets']), 0)
        self.assertEqual({t['kind'] for t in data['tasks']}, {'learn','revision','practice'})
        quick = self.post('plans/', self.payload(mode='revision')).json()
        self.assertEqual(quick['total_minutes'], 150)

    def test_completed_task_history_survives_edit_reschedule_and_other_user_cannot_access(self):
        data = self.post('plans/', self.payload()).json(); pk = data['id']; task = data['tasks'][0]
        done = self.post(f'plans/{pk}/tasks/{task["id"]}/', {'is_completed': True}).json()
        historic = StudyTask.objects.get(pk=task['id']); before = (historic.minutes, historic.completed_at)
        changed = self.post(f'plans/{pk}/reschedule/', {'revision': done['revision'], 'start_date': '2026-11-02'})
        self.assertEqual(changed.status_code, 200)
        historic.refresh_from_db(); self.assertEqual((historic.minutes, historic.completed_at), before)
        self.assertEqual(changed.json()['total_minutes'], data['total_minutes'])
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f'/api/plans/{pk}/').status_code, 404)
        self.assertEqual(self.post(f'plans/{pk}/tasks/{task["id"]}/', {'is_completed': False}).status_code, 404)
        self.assertEqual(self.client.get('/api/plans/').json(), [])

    def test_invalid_days_dates_hours_unknown_drafts_and_stale_edits_fail_cleanly(self):
        for change in ({'study_days': []}, {'study_days': [True]}, {'study_days': [0,0]}, {'daily_minutes': '60'}, {'daily_minutes': 0}, {'start_date': 'bad'}, {'exam_date': '2026-01-01'}, {'topic_ids': [999999]}):
            self.assertEqual(self.post('plans/', self.payload(**change)).status_code, 400)
        self.assertEqual(StudyPlan.objects.count(), 0)
        data = self.post('plans/', self.payload()).json()
        self.assertEqual(self.post(f'plans/{data["id"]}/', {**self.payload(), 'revision': 0}).status_code, 409)
        self.assertEqual(self.client.get('/api/plans/').status_code, 200)
        self.assertEqual(self.client.get('/api/dashboard/').json()['study_plans'][0]['id'], data['id'])

import uuid
from .models import Question, Choice
from .services.quiz import review_quiz


class SavedPracticeTests(OwnedTopicStateTests):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.question=Question.objects.create(quiz=cls.quiz,primary_topic=cls.lessons[0],question_text='Original reviewed question?',explanation='Original reviewed explanation.')
        cls.correct=Choice.objects.create(question=cls.question,choice_text='Supported answer',is_correct=True)
        Choice.objects.create(question=cls.question,choice_text='Other answer')
        review_quiz(cls.quiz,cls.editor,'Synthetic reviewed fixture')

    def submission(self):
        preview=self.client.get('/api/topic/lesson-0/quiz/').json()
        return {'quiz_id':preview['id'],'revision_token':preview['revision_token'],'answers':{str(self.question.pk):self.correct.pk},'submission_id':str(uuid.uuid4())}

    def test_saved_snapshot_idempotence_history_survives_edit_and_question_deletion(self):
        payload=self.submission()
        first=self.post('topic/lesson-0/quiz/submit/',payload)
        self.assertEqual(first.status_code,200,first.json())
        again=self.post('topic/lesson-0/quiz/submit/',payload)
        self.assertEqual(first.json(),again.json());self.assertEqual(QuizAttempt.objects.count(),1)
        self.question.question_text='Edited question';self.question.save()
        pk=first.json()['attempt_id'];self.question.delete()
        data=self.client.get(f'/api/attempts/{pk}/').json()
        self.assertEqual(data['snapshot']['questions'][0]['question_text'],'Original reviewed question?')
        self.assertEqual(data['snapshot']['questions'][0]['choices'][0]['choice_text'],'Supported answer')
        self.assertEqual(data['score'],1)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f'/api/attempts/{pk}/').status_code,404)
        self.assertEqual(self.client.get('/api/attempts/').json()['count'],0)

    def test_invalid_membership_formats_and_changed_submission_do_not_create_rows(self):
        payload=self.submission()
        for changes in ({'answers':{'999999':self.correct.pk}},{'answers':{str(self.question.pk):True}},{'submission_id':'bad'}):
            self.assertEqual(self.post('topic/lesson-0/quiz/submit/',{**payload,**changes}).status_code,400)
        self.assertFalse(QuizAttempt.objects.exists())
        self.assertEqual(self.post('topic/lesson-0/quiz/submit/',payload).status_code,200)
        self.assertEqual(self.post('topic/lesson-0/quiz/submit/',{**payload,'answers':{}}).status_code,409)
        self.assertEqual(QuizAttempt.objects.count(),1)

    def test_guest_check_stays_stateless_and_guest_submit_is_denied(self):
        payload=self.submission();self.client.logout()
        stateless={k:v for k,v in payload.items() if k!='submission_id'}
        self.assertEqual(self.post('topic/lesson-0/quiz/check/',stateless).status_code,200)
        self.assertEqual(self.post('topic/lesson-0/quiz/submit/',payload).status_code,401)
        self.assertFalse(QuizAttempt.objects.exists())

    def test_subject_collection_attempt_and_weighted_subject_accuracy(self):
        preview=self.client.get('/api/topic/subject/practice/').json()
        payload={k:preview[k] for k in ('collection_id','page','revision_token')}
        payload.update(answers={},submission_id=str(uuid.uuid4()))
        response=self.post('topic/subject/practice/submit/',payload)
        self.assertEqual(response.status_code,200,response.json())
        dashboard=self.client.get('/api/dashboard/').json()
        self.assertEqual(dashboard['subject_performance'][0]['accuracy'],0)
        self.assertEqual(dashboard['stats']['total_quizzes_taken'],1)
        self.assertEqual(self.client.get('/api/profile/weaknesses/').json()['weaknesses'][0]['topic_id'],self.lessons[0].pk)
