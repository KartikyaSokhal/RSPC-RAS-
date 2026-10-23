"""Staging access barrier and explicit SPA entry points; never serve arbitrary paths."""
import base64
import binascii
from django.conf import settings
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.utils.crypto import constant_time_compare
from django.views.decorators.http import require_safe


class StagingAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Readiness only; no account/content endpoint is exempt.
        if request.path == '/api/health/' and request.method in ('GET', 'HEAD'):
            request.META.pop('HTTP_AUTHORIZATION', None)
            request.__dict__.pop('headers', None)
            return self.get_response(request)
        user = password = ''
        scheme, _, payload = request.headers.get('Authorization', '').partition(' ')
        if scheme.lower() == 'basic':
            try:
                user, separator, password = base64.b64decode(payload, validate=True).decode('utf-8').partition(':')
                if not separator: user = password = ''
            except (ValueError, UnicodeError, binascii.Error):
                pass
        valid = constant_time_compare(user, settings.STAGING_ACCESS_USERNAME) & constant_time_compare(password, settings.STAGING_ACCESS_PASSWORD)
        if not valid or not settings.STAGING_ACCESS_USERNAME or not settings.STAGING_ACCESS_PASSWORD:
            response = HttpResponse('Restricted staging environment.', status=401)
            response['WWW-Authenticate'] = 'Basic realm="Prepal staging", charset="UTF-8"'
        else:
            # This credential protects staging, not a Django/DRF student identity.
            request.META.pop('HTTP_AUTHORIZATION', None)
            request.__dict__.pop('headers', None)  # Refresh Django's cached header mapping for DRF.
            response = self.get_response(request)
        response['Cache-Control'] = 'private, no-store'
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response


@require_safe
def frontend(request, **kwargs):
    index = settings.FRONTEND_ROOT / 'index.html'
    if not index.is_file():
        return HttpResponseNotFound('Frontend build unavailable.')
    response = FileResponse(index.open('rb'), content_type='text/html')
    response['Cache-Control'] = 'no-store'
    response['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; worker-src 'self' blob:; frame-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
    return response
