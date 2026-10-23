"""Synthetic same-origin staging delivery/security tests; no hosted credentials."""
import base64
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from django.conf import settings
from django.test import SimpleTestCase, TestCase, override_settings


class RenderConfigurationTests(SimpleTestCase):
    def test_profile_fails_closed_and_keeps_production_security(self):
        env = {**os.environ, 'PYTHON_DOTENV_DISABLED': '1', 'DJANGO_ENV': 'production',
               'PREPAL_ENVIRONMENT': 'staging', 'SECRET_KEY': 'synthetic-test-only-never-used-as-a-real-key-12345678901234567890',
               'DEBUG': 'false', 'ALLOWED_HOSTS': 'staging.example.invalid',
               'SITE_ORIGIN': 'https://staging.example.invalid', 'DATABASE_ENGINE': 'postgresql',
               'POSTGRES_DB': 'synthetic', 'POSTGRES_USER': 'synthetic', 'POSTGRES_HOST': 'db.example.invalid',
               'POSTGRES_PASSWORD': 'synthetic', 'POSTGRES_SSLMODE': 'verify-full',
               'STAGING_ACCESS_USERNAME': 'reviewer', 'STAGING_ACCESS_PASSWORD': 'synthetic-access-test-only-12345',
               'PRIVATE_MEDIA_ROOT': '/var/data/prepal-media', 'STUDENT_FEATURES_ENABLED': 'true', 'AI_ENABLED': 'true'}
        command = [sys.executable, '-c', 'import core.render_settings as s; assert not s.STUDENT_FEATURES_ENABLED and not s.AI_ENABLED; assert s.SESSION_COOKIE_SECURE and s.CSRF_COOKIE_SECURE; assert not s.CORS_ALLOWED_ORIGINS']
        backend = Path(__file__).resolve().parents[1]
        self.assertEqual(subprocess.run(command, cwd=backend, env=env, capture_output=True).returncode, 0)
        for invalid in ({'STAGING_ACCESS_PASSWORD': ''}, {'SITE_ORIGIN': 'http://staging.example.invalid'},
                        {'PRIVATE_MEDIA_ROOT': str(backend/'private-media')}, {'POSTGRES_SSLMODE': 'require'},
                        {'PREPAL_ENVIRONMENT': 'production'}):
            self.assertNotEqual(subprocess.run(command, cwd=backend, env=env | invalid, capture_output=True).returncode, 0)

        opted_in = env | {'PREPAL_STAGING_STUDENT_TESTS': 'true', 'PREPAL_STAGING_SYNTHETIC_DATA': 'true', 'POSTGRES_DB': 'prepal_staging_synthetic'}
        command = [sys.executable, '-c', 'import core.render_settings as s; assert s.STUDENT_FEATURES_ENABLED and not s.AI_ENABLED and not s.GOOGLE_CLIENT_ID']
        self.assertEqual(subprocess.run(command, cwd=backend, env=opted_in, capture_output=True).returncode, 0)
        for invalid in ({'PREPAL_STAGING_SYNTHETIC_DATA': 'false'}, {'POSTGRES_DB': 'valuable'}, {'STAGING_ACCESS_PASSWORD': ''}):
            self.assertNotEqual(subprocess.run(command, cwd=backend, env=opted_in | invalid, capture_output=True).returncode, 0)


class RenderDeliveryTests(TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        (root / 'index.html').write_text('<html><body><div id="root">Synthetic SPA</div></body></html>')
        (root / 'asset.js').write_text('console.log("synthetic static")')
        (root / 'static').mkdir()
        (root / 'static/admin.css').write_text('body { color: black; }')
        password = 'synthetic-staging-access-only-12345'
        middleware = list(settings.MIDDLEWARE)
        position = middleware.index('django.middleware.security.SecurityMiddleware') + 1
        middleware[position:position] = ['core.render_support.StagingAccessMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware']
        self.config = override_settings(ROOT_URLCONF='core.render_urls', FRONTEND_ROOT=root,
            WHITENOISE_ROOT=root, STATIC_ROOT=root/'static', STATIC_URL='/static/',
            WHITENOISE_AUTOREFRESH=False, WHITENOISE_USE_FINDERS=False,
            MIDDLEWARE=middleware, STAGING_ACCESS_USERNAME='reviewer', STAGING_ACCESS_PASSWORD=password,
            SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True,
            SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'))
        self.config.enable(); self.addCleanup(self.config.disable)
        self.authorization = 'Basic ' + base64.b64encode(f'reviewer:{password}'.encode()).decode()

    def get(self, path, **kwargs):
        return self.client.get(path, HTTP_AUTHORIZATION=self.authorization, secure=True, **kwargs)

    def test_staging_access_required_for_spa_admin_api_and_assets(self):
        for path in ('/', '/dashboard', '/admin/login/', '/api/config/', '/asset.js', '/static/admin.css'):
            for authorization in ('', 'Basic invalid%%%', 'Basic d3Jvbmc6d3Jvbmc='):
                response = self.client.get(path, secure=True, HTTP_AUTHORIZATION=authorization)
                self.assertEqual(response.status_code, 401, path)
                self.assertIn('no-store', response['Cache-Control'])
        self.assertEqual(self.client.get('/api/health/', secure=True).status_code, 200)

    def test_spa_routes_and_security_headers(self):
        for path in ('/', '/search', '/dashboard', '/topic/rajasthan', '/tags/history', '/resources/1'):
            response = self.get(path)
            self.assertEqual(response.status_code, 200, path)
            self.assertIn(b'Synthetic SPA', b''.join(response.streaming_content))
            self.assertIn("script-src 'self'", response['Content-Security-Policy'])
            self.assertIn('noindex', response['X-Robots-Tag'])
        self.assertEqual(self.client.post('/dashboard', HTTP_AUTHORIZATION=self.authorization, secure=True).status_code, 405)

    def test_assets_admin_and_real_api_not_spa_fallback(self):
        self.assertEqual(self.get('/asset.js').status_code, 200)
        self.assertEqual(self.get('/static/admin.css').status_code, 200)
        self.assertEqual(self.get('/admin/login/').status_code, 200)
        response = self.get('/api/config/')
        self.assertFalse(response.json()['student_features_enabled'])
        self.assertTrue(response.cookies['csrftoken']['secure'])
        self.assertEqual(response.cookies['csrftoken']['samesite'], 'Lax')
        for path in ('/api/missing/', '/private-media/secret.pdf', '/.env', '/backend/db.sqlite3', '/.git/config', '/assets/missing.js'):
            self.assertEqual(self.get(path).status_code, 404, path)

    def test_staging_basic_credentials_do_not_authenticate_student(self):
        with override_settings(STUDENT_FEATURES_ENABLED=True):
            self.assertFalse(self.get('/api/auth/status/').json()['authenticated'])
        self.assertEqual(self.get('/api/auth/status/').status_code, 503)
