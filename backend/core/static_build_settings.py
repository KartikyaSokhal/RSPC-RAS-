"""Static collection only: no dotenv, real database or runtime signing credentials."""
import os
import secrets
from unittest.mock import patch
with patch('dotenv.load_dotenv'), patch.dict(os.environ, {
    'DJANGO_ENV': 'development', 'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': ':memory:',
    'SECRET_KEY': secrets.token_urlsafe(64), 'AI_ENABLED': 'false', 'AI_GUEST_ENABLED': 'false',
    'STUDENT_FEATURES_ENABLED': 'false',
}):
    from .settings import *  # noqa: F403
DATABASES = {'default': {'ENGINE': 'django.db.backends.dummy'}}
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STORAGES = {'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
