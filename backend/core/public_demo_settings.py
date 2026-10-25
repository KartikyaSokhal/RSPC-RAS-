"""LOCAL synthetic student preview. Never select this profile on Render."""
import json
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

os.environ['PYTHON_DOTENV_DISABLED'] = '1'
from .local_postgres_settings import *  # noqa: F403,E402

config = DATABASES['default']
root_value = os.environ.get('PREPAL_DEMO_ROOT', '')
if (os.environ.get('PREPAL_PUBLIC_DEMO') != '1' or os.environ.get('RENDER')
        or not config['NAME'].startswith('prepal_local_public_demo_') or not root_value):
    raise ImproperlyConfigured('Public demo requires an explicitly prepared LOCAL synthetic PostgreSQL database.')
DEMO_ROOT = Path(root_value).resolve()
marker = DEMO_ROOT / '.public-demo.json'
try:
    state = json.loads(marker.read_text()) if not marker.is_symlink() else {}
except (OSError, ValueError):
    state = {}
if state != {'kind': 'prepal-local-public-demo-v1', 'state': 'ready', 'database': config['NAME']}:
    raise ImproperlyConfigured('Prepare a NEW local public demo first; never adopt existing student data.')

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:5173', 'http://localhost:5173', 'http://127.0.0.1:4175']
DEMO_MODE = True
STUDENT_FEATURES_ENABLED = True
LEARNING_AUTH_REQUIRED = True
STUDENT_REGISTRATION_ENABLED = False
PASSWORD_RESET_ENABLED = False
SUPPORT_EMAIL = ''
GOOGLE_CLIENT_ID = GOOGLE_CLIENT_SECRET = GOOGLE_REDIRECT_URI = ''
AI_ENABLED = AI_GUEST_ENABLED = False
GEMINI_API_KEY = ''
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
MEDIA_ROOT = DEMO_ROOT / 'media'
STATIC_ROOT = DEMO_ROOT / 'static'
FILE_UPLOAD_HANDLERS = ['core.free_demo_support.RejectUploadHandler']
STORAGES = {'default': {'BACKEND': 'core.free_demo_support.DisabledUploadStorage'},
            'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}}
MIDDLEWARE = [*MIDDLEWARE, 'core.public_demo_support.StudentLearningAccessMiddleware']
REST_FRAMEWORK = {**REST_FRAMEWORK, 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication']}
