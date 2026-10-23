"""Explicit local PostgreSQL candidate, never selected by the active SQLite demo."""
import os
from django.core.exceptions import ImproperlyConfigured
from .settings import *  # noqa: F403

config = DATABASES['default']
if (PRODUCTION or os.environ.get('PREPAL_LOCAL_POSTGRES') != '1'
        or config['ENGINE'] != 'django.db.backends.postgresql'
        or config['HOST'] not in ('127.0.0.1', 'localhost', '::1')
        or not config['NAME'].startswith(('prepal_local_', 'prepal_rehearsal_'))):
    raise ImproperlyConfigured('Select an explicit disposable/local PostgreSQL candidate; never an implicit cutover.')
GOOGLE_CLIENT_ID = GOOGLE_CLIENT_SECRET = GOOGLE_REDIRECT_URI = ''
AI_ENABLED = AI_GUEST_ENABLED = False
GEMINI_API_KEY = ''
