"""Explicit, access-restricted Render staging; does not activate production learners."""
import os
from urllib.parse import urlsplit
from django.core.exceptions import ImproperlyConfigured
from .staging_settings import *  # noqa: F403

ROOT_URLCONF = 'core.render_urls'
FRONTEND_ROOT = BASE_DIR.parent / 'dist'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
WHITENOISE_ROOT = FRONTEND_ROOT
WHITENOISE_AUTOREFRESH = False
WHITENOISE_USE_FINDERS = False
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
MIDDLEWARE = list(MIDDLEWARE)
position = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1
MIDDLEWARE[position:position] = ['core.render_support.StagingAccessMiddleware',
                                'whitenoise.middleware.WhiteNoiseMiddleware']
STAGING_ACCESS_USERNAME = os.getenv('STAGING_ACCESS_USERNAME', '')
STAGING_ACCESS_PASSWORD = os.getenv('STAGING_ACCESS_PASSWORD', '')
if not STAGING_ACCESS_USERNAME or ':' in STAGING_ACCESS_USERNAME or len(STAGING_ACCESS_PASSWORD) < 24:
    raise ImproperlyConfigured('Render staging requires private access credentials (password at least 24 characters).')
origin = urlsplit(SITE_ORIGIN)
if origin.scheme != 'https' or not origin.hostname or origin.username or origin.password or origin.path not in ('', '/') or origin.query or origin.fragment or origin.netloc not in ALLOWED_HOSTS:
    raise ImproperlyConfigured('SITE_ORIGIN must be the exact approved HTTPS host in ALLOWED_HOSTS.')
CSRF_TRUSTED_ORIGINS = [SITE_ORIGIN.rstrip('/')]
CORS_ALLOWED_ORIGINS = []  # Browser, Admin and API share the same origin.
SESSION_COOKIE_DOMAIN = CSRF_COOKIE_DOMAIN = None
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Do not trust client IP headers until Render proxy overwrite behavior is verified.
TRUSTED_PROXY_IPS = ()
MEDIA_ROOT = MEDIA_ROOT.resolve()
if not MEDIA_ROOT.is_absolute() or MEDIA_ROOT == BASE_DIR / 'private-media' or MEDIA_ROOT.is_relative_to(BASE_DIR.parent):
    raise ImproperlyConfigured('PRIVATE_MEDIA_ROOT must be an absolute persistent mount outside the checkout.')
# Authorized staging acceptance only; never enable via the general production flag.
if os.getenv('PREPAL_STAGING_STUDENT_TESTS') == 'true':
    if os.getenv('PREPAL_STAGING_SYNTHETIC_DATA') != 'true' or not DATABASES['default']['NAME'].startswith('prepal_staging_'):
        raise ImproperlyConfigured('Staging learner tests require an explicitly synthetic prepal_staging_ database.')
    STUDENT_FEATURES_ENABLED = True
