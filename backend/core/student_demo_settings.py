"""NEW isolated review database only; existing demos are never upgraded in place."""
from .demo_settings import *  # noqa: F403
import json
from django.core.exceptions import ImproperlyConfigured
marker = DEMO_ROOT / '.student-demo.json'
if not os.environ.get('PREPAL_DEMO_ROOT') or not marker.is_file() or marker.is_symlink():
    raise ImproperlyConfigured('Prepare a NEW isolated student-review demo first.')
record = json.loads(marker.read_text())
if record.get('kind') != 'prepal-student-review-v2' or record.get('state') not in ('preparing', 'ready'):
    raise ImproperlyConfigured('Invalid isolated student-review marker.')
STUDENT_FEATURES_ENABLED = True
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
GOOGLE_CLIENT_ID = GOOGLE_CLIENT_SECRET = GOOGLE_REDIRECT_URI = ''
