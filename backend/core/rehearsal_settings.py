"""Internal settings for newly created local PostgreSQL rehearsal databases only."""
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

if os.environ.get('PREPAL_REHEARSAL') != '1' or os.environ.get('PYTHON_DOTENV_DISABLED') != '1':
    raise ImproperlyConfigured('Rehearsal settings require explicit isolation.')

from .settings import *  # noqa: F403,E402

config = DATABASES['default']
if (config['ENGINE'] != 'django.db.backends.postgresql'
        or config['HOST'] not in ('127.0.0.1', 'localhost', '::1')
        or not config['NAME'].startswith('prepal_rehearsal_')):
    raise ImproperlyConfigured('Rehearsal requires a new local prepal_rehearsal_* PostgreSQL database.')
source = Path(os.environ['PREPAL_REHEARSAL_COPY']).resolve()
if source.name != 'migration-copy.sqlite3' or not source.is_file():
    raise ImproperlyConfigured('A migrated disposable SQLite copy is required.')
DATABASES['source_copy'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': source.as_uri() + '?mode=ro', 'OPTIONS': {'uri': True},
}
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
AI_ENABLED = False
AI_GUEST_ENABLED = False
GEMINI_API_KEY = ''
