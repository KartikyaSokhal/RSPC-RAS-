"""Restricted, text-only Render Free demonstration; never a production profile."""
import os
import re
from pathlib import Path
import tempfile
import certifi
from django.core.exceptions import ImproperlyConfigured

if (os.getenv('DJANGO_ENV') != 'production' or os.getenv('PREPAL_ENVIRONMENT') != 'free-demo'
        or os.getenv('PREPAL_FREE_DEMO') != '1' or os.getenv('PREPAL_FREE_DEMO_SYNTHETIC_DATA') != '1'
        or os.getenv('PYTHON_DOTENV_DISABLED') != '1'):
    raise ImproperlyConfigured('Free demo requires explicit production security, free-demo environment, both demo acknowledgements and disabled dotenv loading.')

from .settings import *  # noqa: F403,E402

# Preserve the shared production database policy, including verify-full. Render's
# internal self-signed endpoint cannot meet it; only its external TLS endpoint can.
if not re.fullmatch(r'dpg-[a-z0-9-]+\.[a-z0-9-]+-postgres\.render\.com', DATABASES['default']['HOST']):
    raise ImproperlyConfigured('Free demo requires the full external Render PostgreSQL hostname for verified TLS.')
ca = Path(os.getenv('POSTGRES_SSLROOTCERT') or certifi.where()).expanduser()
if not ca.is_file():
    raise ImproperlyConfigured('Free demo requires an existing trusted PostgreSQL CA bundle.')
DATABASES['default']['OPTIONS']['sslrootcert'] = str(ca)
DATABASES['default']['CONN_MAX_AGE'] = 0

FREE_DEMO_READ_ONLY = DEMO_MODE = True
STUDENT_FEATURES_ENABLED = AI_ENABLED = AI_GUEST_ENABLED = False
GOOGLE_CLIENT_ID = GOOGLE_CLIENT_SECRET = GOOGLE_REDIRECT_URI = ''
GEMINI_API_KEY = AI_MODEL = ''
AI_DAILY_BUDGET_MICRO = AI_INPUT_RATE_MICRO = AI_OUTPUT_RATE_MICRO = 0
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Reuse the reviewed same-origin delivery/barrier without importing its mandatory
# paid-disk staging profile or altering either staging or production settings.
from urllib.parse import urlsplit  # noqa: E402
origin = urlsplit(SITE_ORIGIN)
if (origin.scheme != 'https' or not origin.hostname or origin.username or origin.password
        or origin.path not in ('', '/') or origin.query or origin.fragment or origin.netloc not in ALLOWED_HOSTS):
    raise ImproperlyConfigured('Free demo requires the exact HTTPS SITE_ORIGIN in ALLOWED_HOSTS.')
STAGING_ACCESS_USERNAME = os.getenv('STAGING_ACCESS_USERNAME', '')
STAGING_ACCESS_PASSWORD = os.getenv('STAGING_ACCESS_PASSWORD', '')
if not STAGING_ACCESS_USERNAME or ':' in STAGING_ACCESS_USERNAME or len(STAGING_ACCESS_PASSWORD) < 24:
    raise ImproperlyConfigured('Free demo requires the existing private staging access barrier.')
CSRF_TRUSTED_ORIGINS = [SITE_ORIGIN.rstrip('/')]
CORS_ALLOWED_ORIGINS = []
SESSION_COOKIE_DOMAIN = CSRF_COOKIE_DOMAIN = None
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
TRUSTED_PROXY_IPS = ()
ROOT_URLCONF = 'core.free_demo_urls'
FRONTEND_ROOT = BASE_DIR.parent / 'dist'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
WHITENOISE_ROOT = FRONTEND_ROOT
WHITENOISE_AUTOREFRESH = WHITENOISE_USE_FINDERS = False
MIDDLEWARE = list(MIDDLEWARE)
position = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1
MIDDLEWARE[position:position] = ['core.render_support.StagingAccessMiddleware',
                                'core.free_demo_support.FreeDemoRestrictions',
                                'whitenoise.middleware.WhiteNoiseMiddleware']
STORAGES = {
    'default': {'BACKEND': 'core.free_demo_support.DisabledUploadStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
# No upload directory is created or used. Keep existing PRIVATE_MEDIA_ROOT env
# intact but do not read/write its data from this disposable demonstration.
MEDIA_ROOT = Path(tempfile.gettempdir()) / 'prepal-free-demo-uploads-disabled'
FILE_UPLOAD_HANDLERS = ['core.free_demo_support.RejectUploadHandler']
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FILES = 0
