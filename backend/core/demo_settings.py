"""Loopback-only synthetic demo. Cannot use the real database or live provider."""
import os
from pathlib import Path
from unittest.mock import patch
os.environ['PYTHON_DOTENV_DISABLED'] = '1'
with patch('dotenv.load_dotenv'), patch.dict(os.environ, {
    'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': ':memory:', 'DJANGO_ENV': 'development',
}):
    from .settings import *  # noqa: F403

DEMO_MODE = True
PRODUCTION = False
DEBUG = True
SECRET_KEY = 'synthetic-local-demo-only-not-for-production-000000000000'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
DEMO_ROOT = Path(os.environ.get('PREPAL_DEMO_ROOT', str(Path(__file__).resolve().parents[2] / '.local' / 'demo'))).resolve()
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': DEMO_ROOT / 'demo.sqlite3', 'OPTIONS': {'timeout': 5}}}
MEDIA_ROOT = DEMO_ROOT / 'media'
STATIC_ROOT = DEMO_ROOT / 'static'
AI_ENABLED = True
AI_GUEST_ENABLED = True
GEMINI_API_KEY = ''
AI_MODEL = 'mock-demo-no-network'
AI_DAILY_BUDGET_MICRO = 1000000
AI_INPUT_RATE_MICRO = 1000000
AI_OUTPUT_RATE_MICRO = 1000000
AI_VISITOR_DAILY_LIMIT = 200
AI_IP_DAILY_LIMIT = 1000
AI_MINUTE_LIMIT = 30
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:5173', 'http://localhost:5173', 'http://127.0.0.1:4173', 'http://127.0.0.1:4175']
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SUPPORT_EMAIL = ''

# Preserve the existing content-only demo and its historical learner boundary.
STUDENT_FEATURES_ENABLED = False
