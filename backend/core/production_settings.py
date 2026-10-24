"""Unactivated production profile; no student release is approved by local setup."""
import os
from django.core.exceptions import ImproperlyConfigured
if os.environ.get('DJANGO_ENV') != 'production' or os.environ.get('PREPAL_ENVIRONMENT') != 'production':
    raise ImproperlyConfigured('Production requires its own explicitly selected private environment.')
from .settings import *  # noqa: F403,E402
STUDENT_FEATURES_ENABLED = False
AI_ENABLED = AI_GUEST_ENABLED = False
GOOGLE_CLIENT_ID = GOOGLE_CLIENT_SECRET = GOOGLE_REDIRECT_URI = ''
