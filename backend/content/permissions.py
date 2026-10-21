"""Temporary P002 boundary: no identity can access ownerless learner state."""
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


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
