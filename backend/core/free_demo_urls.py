"""Free-demo readiness precedes the shared reviewed SPA/API/Admin routes."""
from django.urls import path
from .free_demo_support import health
from .render_urls import urlpatterns as shared_urls

urlpatterns = [path('api/health/', health), *shared_urls]
