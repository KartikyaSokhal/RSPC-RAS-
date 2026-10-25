"""No hosted SQL: strict configuration and HTTPS visitor/session boundaries."""
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase, Client, override_settings
from .models import StudentIdentity, Topic, ContentBlock
from .services.publication import publish


class HostedPublicConfigurationTests(SimpleTestCase):
    def test_profile_is_exact_synthetic_tls_and_has_no_basic_middleware(self):
        env = {**os.environ, 'PYTHON_DOTENV_DISABLED':'1', 'DJANGO_ENV':'production',
               'PREPAL_ENVIRONMENT':'public-demo','PREPAL_PUBLIC_DEMO':'1','PREPAL_FREE_DEMO':'1',
               'PREPAL_FREE_DEMO_SYNTHETIC_DATA':'1', 'SECRET_KEY':'synthetic-public-config-only-not-used-for-hosted-signing-1234567890',
               'DEBUG':'false','ALLOWED_HOSTS':'rspc-ras.onrender.com','SITE_ORIGIN':'https://rspc-ras.onrender.com',
               'DATABASE_ENGINE':'postgresql','POSTGRES_HOST':'dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com',
               'POSTGRES_DB':'prepal_staging_db','POSTGRES_PORT':'5432','POSTGRES_USER':'prepal_demo_runtime','POSTGRES_PASSWORD':'synthetic-unused',
               'POSTGRES_SSLMODE':'verify-full','POSTGRES_SSLROOTCERT':'', 'STAGING_ACCESS_USERNAME':'','STAGING_ACCESS_PASSWORD':'',
               'STUDENT_FEATURES_ENABLED':'true','AI_ENABLED':'true','GOOGLE_CLIENT_ID':'unused-synthetic'}
        code = '''import core.render_public_demo_settings as s
assert s.PRODUCTION and not s.DEBUG and s.LEARNING_AUTH_REQUIRED and s.STUDENT_FEATURES_ENABLED
assert not s.STUDENT_REGISTRATION_ENABLED and not s.PASSWORD_RESET_ENABLED
assert not s.AI_ENABLED and not s.GEMINI_API_KEY and not s.GOOGLE_CLIENT_ID
assert s.SESSION_COOKIE_SECURE and s.CSRF_COOKIE_SECURE and s.SESSION_COOKIE_HTTPONLY
assert s.SECURE_SSL_REDIRECT and s.SESSION_COOKIE_AGE == 3600
assert s.DATABASES['default']['OPTIONS']['sslmode'] == 'verify-full'
assert s.DATABASES['default']['OPTIONS']['sslrootcert']
assert s.CSRF_TRUSTED_ORIGINS == ['https://rspc-ras.onrender.com']
assert not s.CORS_ALLOWED_ORIGINS and s.SESSION_COOKIE_DOMAIN is None
assert not any('StagingAccessMiddleware' in m for m in s.MIDDLEWARE)
assert s.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] == ['rest_framework.authentication.SessionAuthentication']
'''
        for changes in ({}, {'PREPAL_PUBLIC_DEMO':''}, {'PREPAL_FREE_DEMO_SYNTHETIC_DATA':''},
                        {'PREPAL_ENVIRONMENT':'free-demo'}, {'DJANGO_ENV':'development'},
                        {'POSTGRES_SSLMODE':'require'}, {'POSTGRES_HOST':'127.0.0.1'},
                        {'POSTGRES_DB':'valuable_database'}, {'POSTGRES_USER':'prepal_demo_migration'}, {'POSTGRES_PORT':'5433'}, {'DEBUG':'true'},
                        {'SITE_ORIGIN':'http://rspc-ras.onrender.com'}, {'ALLOWED_HOSTS':'*'},
                        {'POSTGRES_SSLROOTCERT':'/missing/ca'}, {'PYTHON_DOTENV_DISABLED':'0'}):
            result = subprocess.run([sys.executable,'-c',code],cwd=Path(__file__).resolve().parents[1],env=env|changes,capture_output=True)
            self.assertEqual(result.returncode == 0, not changes, str(changes))


@override_settings(STUDENT_FEATURES_ENABLED=True, LEARNING_AUTH_REQUIRED=True,
                   CONTROLLED_DEMO_ONLY=True, STUDENT_REGISTRATION_ENABLED=False,
                   PASSWORD_RESET_ENABLED=False, AI_ENABLED=False, AI_GUEST_ENABLED=False,
                   PRODUCTION=True, SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True,
                   ROOT_URLCONF='core.free_demo_urls', SECURE_SSL_REDIRECT=True,
                   REST_FRAMEWORK={**settings.REST_FRAMEWORK, 'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework.authentication.SessionAuthentication']})
class HostedPublicBoundaryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user('sample-editor',password='Synthetic-Staff-423!',is_staff=True,is_superuser=True)
        cls.reader = User.objects.create_user('prepal-demo-000000000000000000000000',email='prepal-demo-000000000000000000000000@example.invalid',password='Synthetic-Reader-423!')
        cls.other = User.objects.create_user('other',email='other@example.invalid',password='Synthetic-Other-423!')
        for user in (cls.reader, cls.other): StudentIdentity.objects.create(user=user,email=user.email)
        topic = Topic.objects.create(title='Private lesson title',slug='lesson')
        ContentBlock.objects.create(topic=topic,block_type='text',order=1,content='<p>Private synthetic notes.</p>',source_reference='Synthetic fixture')
        publish(topic,cls.staff)

    def setUp(self):
        self.directory = TemporaryDirectory(); self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name); (root/'index.html').write_text('<html><body>Public Prepal shell</body></html>')
        middleware = [*settings.MIDDLEWARE,'core.public_demo_support.StudentLearningAccessMiddleware']
        self.config = override_settings(FRONTEND_ROOT=root,MIDDLEWARE=middleware)
        self.config.enable(); self.addCleanup(self.config.disable)
        self.client = Client(enforce_csrf_checks=True)
        marker=patch('content.services.public_demo_database.read_public_marker',return_value={'version':1,'student_id':self.reader.pk,'username':self.reader.username})
        marker.start();self.addCleanup(marker.stop)

    def post(self, path, data):
        token = self.client.get('/api/config/',secure=True).json()['csrf_token']
        return self.client.post(path,data,content_type='application/json',secure=True,HTTP_X_CSRFTOKEN=token,HTTP_ORIGIN='https://testserver')

    def test_https_home_and_auth_shells_public_but_all_learning_data_denied(self):
        for path in ('/','/login','/signup','/syllabus','/topic/lesson'):
            response=self.client.get(path,secure=True)
            self.assertEqual(response.status_code,200);self.assertNotIn('WWW-Authenticate',response)
            body=b''.join(response.streaming_content)
            self.assertIn(b'Public Prepal shell',body);self.assertNotIn(b'Private',body)
        for path in ('/api/topics/','/api/topic/lesson/','/api/search/?q=lesson','/api/topic/lesson/quiz/','/api/future/'):
            response=self.client.get(path,secure=True)
            self.assertEqual(response.status_code,401);self.assertNotIn('WWW-Authenticate',response)
        self.assertEqual(self.client.get('/').status_code,301)

    def test_controlled_login_secure_cookie_read_and_logout(self):
        self.assertEqual(self.client.post('/api/auth/login/',{},content_type='application/json',secure=True).status_code,403)
        self.assertEqual(self.post('/api/auth/login/',{'username':'prepal-demo-000000000000000000000000','password':'Synthetic-Reader-423!'}).status_code,200)
        cookie=self.client.cookies['sessionid'];self.assertTrue(cookie['secure']);self.assertTrue(cookie['httponly']);self.assertEqual(cookie['samesite'],'Lax')
        self.assertEqual(self.client.get('/api/topic/lesson/',secure=True).status_code,200)
        self.assertEqual(self.post('/api/auth/logout/',{}).status_code,200)
        self.assertEqual(self.client.get('/api/topic/lesson/',secure=True).status_code,401)

    def test_other_synthetic_or_staff_sessions_cannot_enter_student_library(self):
        self.assertEqual(self.post('/api/auth/login/',{'username':'other','password':'Synthetic-Other-423!'}).status_code,401)
        for actor in (self.other,self.staff):
            self.client.force_login(actor)
            self.assertFalse(self.client.get('/api/auth/status/',secure=True).json()['authenticated'])
            self.assertEqual(self.client.get('/api/topics/',secure=True).status_code,401)
        self.assertEqual(self.client.get('/admin/',secure=True).status_code,200)
        self.assertEqual(self.client.post('/admin/content/topic/add/',{},secure=True).status_code,403)

    def test_signup_and_external_services_stay_closed_for_every_identity(self):
        for actor in (None,self.reader,self.staff):
            self.client.logout()
            if actor: self.client.force_login(actor)
            for path in ('/api/auth/register/','/api/auth/google/start/','/api/auth/password-reset/'):
                self.assertEqual(self.post(path,{}).status_code,503)

    def test_cross_origin_login_is_rejected_without_a_basic_challenge(self):
        token=self.client.get('/api/config/',secure=True).json()['csrf_token']
        response=self.client.post('/api/auth/login/',{'username':'prepal-demo-000000000000000000000000','password':'Synthetic-Reader-423!'},content_type='application/json',secure=True,HTTP_X_CSRFTOKEN=token,HTTP_ORIGIN='https://evil.example.invalid')
        self.assertEqual(response.status_code,403);self.assertNotIn('WWW-Authenticate',response)
