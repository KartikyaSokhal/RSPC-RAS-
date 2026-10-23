"""Render-only SPA routing. Unknown API, media and repository paths stay 404."""
from django.urls import path, re_path
from .urls import urlpatterns as backend_urls
from .render_support import frontend

urlpatterns = [*backend_urls, path('', frontend),
    re_path(r'^(?:syllabus|search|about|help|login|signup|planner|reset-password|dashboard)/?$', frontend),
    re_path(r'^(?:topic|quiz|practice|tags|resources|attempts)/[^/.]+/?$', frontend),
]
