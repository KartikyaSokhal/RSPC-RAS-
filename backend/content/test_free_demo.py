"""Synthetic-only free profile: strict TLS, disabled learner/AI and no uploads."""
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import OperationalError
from django.test import SimpleTestCase, override_settings
from core.free_demo_support import DisabledUploadStorage, RejectUploadHandler
from . import test_render


class FreeDemoConfigurationTests(SimpleTestCase):
    def test_only_explicit_synthetic_profile_and_verified_external_tls(self):
        env = {**os.environ, 'PYTHON_DOTENV_DISABLED': '1', 'DJANGO_ENV': 'production',
            'PREPAL_ENVIRONMENT': 'free-demo', 'PREPAL_FREE_DEMO': '1', 'PREPAL_FREE_DEMO_SYNTHETIC_DATA': '1',
            'SECRET_KEY': 'synthetic-configuration-only-key-never-used-for-deployment-1234567890',
            'DEBUG': 'false', 'ALLOWED_HOSTS': 'demo.example.invalid', 'SITE_ORIGIN': 'https://demo.example.invalid',
            'DATABASE_ENGINE': 'postgresql', 'POSTGRES_HOST': 'dpg-synthetic-a.singapore-postgres.render.com',
            'POSTGRES_DB': 'synthetic_demo', 'POSTGRES_USER': 'synthetic', 'POSTGRES_PASSWORD': 'synthetic',
            'POSTGRES_SSLMODE': 'verify-full', 'POSTGRES_SSLROOTCERT': '', 'POSTGRES_CONN_MAX_AGE': '60',
            'STAGING_ACCESS_USERNAME': 'reviewer', 'STAGING_ACCESS_PASSWORD': 'synthetic-access-test-only-12345',
            'STUDENT_FEATURES_ENABLED': 'true', 'AI_ENABLED': 'true', 'AI_GUEST_ENABLED': 'true',
            'PREPAL_STAGING_STUDENT_TESTS': 'true', 'PREPAL_STAGING_SYNTHETIC_DATA': 'true'}
        code = ('import core.free_demo_settings as s; assert not s.DEBUG; '
                'assert not s.STUDENT_FEATURES_ENABLED and not s.AI_ENABLED and not s.AI_GUEST_ENABLED; '
                'assert not s.GEMINI_API_KEY and not s.GOOGLE_CLIENT_ID; '
                'assert s.SESSION_COOKIE_SECURE and s.CSRF_COOKIE_SECURE and s.SECURE_SSL_REDIRECT; '
                'assert s.DATABASES["default"]["OPTIONS"]["sslmode"]=="verify-full"; '
                'assert s.DATABASES["default"]["OPTIONS"]["sslrootcert"]; '
                'assert s.DATABASES["default"]["CONN_MAX_AGE"]==0; '
                'assert s.STORAGES["default"]["BACKEND"].endswith("DisabledUploadStorage")')
        command = [sys.executable, '-c', code]
        backend = Path(__file__).resolve().parents[1]
        self.assertEqual(subprocess.run(command, cwd=backend, env=env, capture_output=True).returncode, 0)
        for invalid in ({'PREPAL_FREE_DEMO': ''}, {'PREPAL_FREE_DEMO_SYNTHETIC_DATA': ''},
                {'PREPAL_ENVIRONMENT': 'production'}, {'DJANGO_ENV': 'development'}, {'DEBUG': 'true'},
                {'PYTHON_DOTENV_DISABLED': ''}, {'POSTGRES_SSLMODE': 'require'}, {'POSTGRES_SSLMODE': 'disable'},
                {'POSTGRES_HOST': 'dpg-synthetic-a'}, {'POSTGRES_SSLROOTCERT': '/missing/demo-ca'},
                {'STAGING_ACCESS_PASSWORD': ''}, {'SITE_ORIGIN': 'http://demo.example.invalid'}):
            self.assertNotEqual(subprocess.run(command, cwd=backend, env=env | invalid, capture_output=True).returncode, 0, tuple(invalid))

    def test_storage_and_handler_never_write_or_read_uploaded_files(self):
        storage = DisabledUploadStorage()
        with self.assertRaises(PermissionDenied): storage.save('private.pdf', ContentFile(b'synthetic'))
        with self.assertRaises(PermissionDenied): storage.delete('private.pdf')
        with self.assertRaises(FileNotFoundError): storage.open('private.pdf')
        with self.assertRaises(ValueError): storage.url('private.pdf')
        with self.assertRaises(PermissionDenied): RejectUploadHandler().new_file()
        self.assertFalse(storage.exists('private.pdf'))


class FreeDemoBoundaryTests(test_render.RenderDeliveryTests):
    def setUp(self):
        super().setUp()
        from django.conf import settings
        middleware = list(settings.MIDDLEWARE)
        middleware.insert(middleware.index('core.render_support.StagingAccessMiddleware')+1,
                          'core.free_demo_support.FreeDemoRestrictions')
        config = override_settings(MIDDLEWARE=middleware, ROOT_URLCONF='core.free_demo_urls',
            STUDENT_FEATURES_ENABLED=False, AI_ENABLED=False, AI_GUEST_ENABLED=False,
            FILE_UPLOAD_HANDLERS=['core.free_demo_support.RejectUploadHandler'])
        config.enable(); self.addCleanup(config.disable)

    def test_admin_edits_and_multipart_uploads_rejected_before_record_changes(self):
        from .models import Topic
        count = Topic.objects.count()
        for url in ('/admin/content/topic/add/', '/admin/content/topic/', '/api/config/'):
            response = self.client.post(url, {'file': SimpleUploadedFile('synthetic.txt', b'demo')},
                HTTP_AUTHORIZATION=self.authorization, secure=True)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json()['error']['code'], 'free_demo_read_only')
        response = self.client.post('/admin/content/topic/add/', {'title': 'Rejected'},
                                   HTTP_AUTHORIZATION=self.authorization, secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Topic.objects.count(), count)
        self.assertEqual(self.get('/admin/login/').status_code, 200)

    def test_student_features_stay_closed_for_guests_and_staff(self):
        from django.contrib.auth import get_user_model
        staff = get_user_model().objects.create_superuser('synthetic-free-staff', password='Synthetic-475-Only!')
        for authenticated in (False, True):
            if authenticated: self.client.force_login(staff)
            for url in ('/api/auth/status/', '/api/dashboard/', '/api/bookmarks/', '/api/progress/', '/api/plans/'):
                response = self.get(url)
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.json()['error']['code'], 'learner_features_unavailable')
            for url in ('/api/auth/register/', '/api/auth/login/', '/api/plans/', '/api/topic/synthetic/progress/'):
                response = self.client.post(url, {}, content_type='application/json', HTTP_AUTHORIZATION=self.authorization, secure=True)
                self.assertEqual(response.status_code, 503)

    def test_tutor_disabled_before_any_provider_call(self):
        with patch('content.services.providers.GeminiProvider.generate') as provider:
            response = self.client.post('/api/topic/synthetic/chat/', {'message': 'Explain'},
                content_type='application/json', HTTP_AUTHORIZATION=self.authorization, secure=True)
        self.assertEqual(response.status_code, 503)
        provider.assert_not_called()

    def test_readiness_is_read_only_and_reports_connection_failure_without_details(self):
        self.assertEqual(self.client.get('/api/health/', secure=True).status_code, 200)
        with patch('django.db.models.query.QuerySet.first', side_effect=OperationalError('private diagnostic')):
            response = self.client.get('/api/health/', secure=True)
        self.assertEqual(response.status_code, 503)
        self.assertNotIn('private diagnostic', response.content.decode())
        self.assertEqual(response.json()['error']['code'], 'demo_database_unavailable')
