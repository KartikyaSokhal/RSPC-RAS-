"""Temporary P002 boundary: no identity can access ownerless learner state."""
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.authentication import SessionAuthentication
from functools import wraps


def unavailable_learner_view(methods):
    """A constant-response endpoint, never a wrapper around the old operation.

    Authentication is deliberately not evaluated: even a session without CSRF,
    invalid credentials or staff identity receives the same unavailable result.
    This is safe only because there is no read/write handler behind this view.
    Restore authentication/CSRF and ownership checks together in P010/P012.
    """
    @api_view(methods)
    @authentication_classes([])
    @permission_classes([AllowAny])
    def unavailable(request, *args, **kwargs):
        return Response({
            "error": {
                "code": "learner_features_unavailable",
                "message": "Student accounts and personalized features are unavailable in this content-first release. Reading and stateless practice remain available.",
            }
        }, status=503, headers={"Cache-Control": "no-store"})

    return unavailable


def student_endpoint(methods):
    """Gate before parsing/authentication; enabled operations restore session CSRF."""
    closed = unavailable_learner_view(['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'])
    def decorate(view):
        protected = csrf_protect(view) if any(m != 'GET' for m in methods) else view
        enabled = api_view(methods)(authentication_classes([SessionAuthentication])(
            permission_classes([AllowAny])(protected)))
        @csrf_exempt
        @wraps(view)
        def dispatch(request, *args, **kwargs):
            if not settings.STUDENT_FEATURES_ENABLED:
                return closed(request, *args, **kwargs)
            return enabled(request, *args, **kwargs)
        return dispatch
    return decorate
