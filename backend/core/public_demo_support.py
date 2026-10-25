"""Session-only, fail-closed learning boundary; no HTTP Basic challenges."""
from django.http import JsonResponse
from django.conf import settings


def is_student(user):
    valid = (user.is_authenticated and user.is_active and not user.is_staff
            and not user.is_superuser and hasattr(user, 'student_identity'))
    if valid and getattr(settings, 'CONTROLLED_DEMO_ONLY', False):
        from content.services.public_demo_database import matches_controlled_student
        return matches_controlled_student(user)
    controlled = getattr(settings, 'CONTROLLED_DEMO_USERNAME', None)
    return valid and (not controlled or (user.username == controlled
        and user.email == controlled+'@example.invalid' and user.student_identity.email == user.email))


class StudentLearningAccessMiddleware:
    PUBLIC = frozenset(('/api/health/', '/api/config/', '/api/auth/login/',
                        '/api/auth/logout/', '/api/auth/status/', '/api/auth/register/'))

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if request.path.startswith('/api/'):
            if request.path.startswith('/api/auth/') and request.path not in self.PUBLIC:
                response = self.error('demo_service_disabled', 'External identity and password recovery are disabled in this synthetic demo.', 503)
            elif request.path not in self.PUBLIC and not is_student(request.user):
                response = self.error('auth_required', 'Sign in to access the learning library.', 401)
        if (request.path.startswith('/admin/') and request.method not in ('GET', 'HEAD', 'OPTIONS')
                and request.path not in ('/admin/login/', '/admin/logout/')):
            response = self.error('demo_read_only', 'Demo administration is read-only.', 403)
        response = response or self.get_response(request)
        response['Cache-Control'] = 'private, no-store'
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response

    @staticmethod
    def error(code, message, status):
        return JsonResponse({'error': {'code': code, 'message': message}}, status=status)
