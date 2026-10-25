"""Unactivated hosted synthetic-login demo; never public enrollment."""
import os
from pathlib import Path
from urllib.parse import urlsplit
import certifi
from django.core.exceptions import ImproperlyConfigured

if (os.getenv('DJANGO_ENV') != 'production' or os.getenv('PREPAL_ENVIRONMENT') != 'public-demo'
        or os.getenv('PREPAL_PUBLIC_DEMO') != '1' or os.getenv('PREPAL_FREE_DEMO') != '1'
        or os.getenv('PREPAL_FREE_DEMO_SYNTHETIC_DATA') != '1'
        or os.getenv('PYTHON_DOTENV_DISABLED') != '1'):
    raise ImproperlyConfigured('Hosted public demo requires explicit production security and synthetic-demo acknowledgements.')

from .settings import *  # noqa: F403,E402
from content.services.free_demo_database import HOST, DATABASE  # noqa: E402

if (DATABASES['default']['HOST'] != HOST or DATABASES['default']['NAME'] != DATABASE
        or DATABASES['default']['PORT'] != '5432' or DATABASES['default']['USER'] != 'prepal_demo_runtime'):
    raise ImproperlyConfigured('Only the existing approved synthetic Render database is eligible.')
ca = Path(os.getenv('POSTGRES_SSLROOTCERT') or certifi.where()).expanduser()
if not ca.is_file():
    raise ImproperlyConfigured('A trusted PostgreSQL CA bundle is mandatory.')
DATABASES['default']['OPTIONS']['sslrootcert'] = str(ca)
DATABASES['default']['CONN_MAX_AGE'] = 0
origin = urlsplit(SITE_ORIGIN)
if SITE_ORIGIN.rstrip('/') != 'https://rspc-ras.onrender.com' or ALLOWED_HOSTS != [origin.netloc]:
    raise ImproperlyConfigured('Use only the existing approved HTTPS demo origin and exact host.')
CSRF_TRUSTED_ORIGINS = [SITE_ORIGIN.rstrip('/')]
CORS_ALLOWED_ORIGINS = []
SESSION_COOKIE_DOMAIN = CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_AGE = 3600
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
TRUSTED_PROXY_IPS = ()

DEMO_MODE = STUDENT_FEATURES_ENABLED = LEARNING_AUTH_REQUIRED = True
CONTROLLED_DEMO_ONLY = True
STUDENT_REGISTRATION_ENABLED = PASSWORD_RESET_ENABLED = False
AI_ENABLED = AI_GUEST_ENABLED = False
GOOGLE_CLIENT_ID = GOOGLE_CLIENT_SECRET = GOOGLE_REDIRECT_URI = ''
GEMINI_API_KEY = AI_MODEL = ''
AI_DAILY_BUDGET_MICRO = AI_INPUT_RATE_MICRO = AI_OUTPUT_RATE_MICRO = 0
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
SUPPORT_EMAIL = ''
ROOT_URLCONF = 'core.free_demo_urls'
FRONTEND_ROOT = BASE_DIR.parent / 'dist'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
WHITENOISE_ROOT = FRONTEND_ROOT
WHITENOISE_AUTOREFRESH = WHITENOISE_USE_FINDERS = False
MIDDLEWARE = list(MIDDLEWARE)
MIDDLEWARE.insert(MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1,
                  'core.public_demo_support.StudentLearningAccessMiddleware')
MIDDLEWARE.insert(MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
                  'core.free_demo_support.FreeDemoRestrictions')
MIDDLEWARE.insert(MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 2,
                  'whitenoise.middleware.WhiteNoiseMiddleware')
REST_FRAMEWORK = {**REST_FRAMEWORK, 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication']}
STORAGES = {'default': {'BACKEND': 'core.free_demo_support.DisabledUploadStorage'},
            'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
MEDIA_ROOT = BASE_DIR / 'uploads-disabled'
FILE_UPLOAD_HANDLERS = ['core.free_demo_support.RejectUploadHandler']
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FILES = 0
