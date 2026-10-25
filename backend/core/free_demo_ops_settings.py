"""Explicit operator-only settings. Never selected by application startup."""
import os
if os.environ.get('PREPAL_FREE_DEMO_LOCAL_TEST') == '1':
    from .settings import *  # noqa: F403
    from content.services.free_demo_database import target
    target(os.environ, local=True)
    DEMO_MODE=True
    STUDENT_FEATURES_ENABLED=AI_ENABLED=AI_GUEST_ENABLED=False
    ROOT_URLCONF='core.free_demo_urls'
    EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend'
    STAGING_ACCESS_USERNAME=os.environ['STAGING_ACCESS_USERNAME']
    STAGING_ACCESS_PASSWORD=os.environ['STAGING_ACCESS_PASSWORD']
    MIDDLEWARE=list(MIDDLEWARE)
    at=MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')+1
    MIDDLEWARE[at:at]=['core.render_support.StagingAccessMiddleware','core.free_demo_support.FreeDemoRestrictions']
else:
    from .free_demo_settings import *  # noqa: F403
