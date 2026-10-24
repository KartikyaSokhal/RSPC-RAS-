"""Unactivated staging profile; independent environment, TLS and credentials required."""
import os
from django.core.exceptions import ImproperlyConfigured
if os.environ.get('DJANGO_ENV') != 'production' or os.environ.get('PREPAL_ENVIRONMENT') != 'staging':
    raise ImproperlyConfigured('Staging requires explicit production security settings and its own environment.')
from .settings import *  # noqa: F403,E402
STUDENT_FEATURES_ENABLED = False  # Acceptance and activation require separate owner approval.
AI_ENABLED = AI_GUEST_ENABLED = False
GOOGLE_CLIENT_ID = GOOGLE_CLIENT_SECRET = GOOGLE_REDIRECT_URI = ''
