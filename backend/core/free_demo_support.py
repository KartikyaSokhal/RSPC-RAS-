"""Free-demo-only restrictions. No filesystem uploads or editorial mutations."""
from django.core.exceptions import PermissionDenied
from django.core.files.storage import Storage
from django.core.files.uploadhandler import FileUploadHandler
from django.http import JsonResponse
from django.db import DatabaseError
from django.views.decorators.http import require_safe


class DisabledUploadStorage(Storage):
    def _save(self, name, content):
        raise PermissionDenied('Uploads are disabled in the free demonstration.')

    def _open(self, name, mode='rb'):
        raise FileNotFoundError('Uploaded media is unavailable in the free demonstration.')

    def exists(self, name):
        return False

    def delete(self, name):
        raise PermissionDenied('Media changes are disabled in the free demonstration.')

    def size(self, name):
        raise FileNotFoundError('Uploaded media is unavailable in the free demonstration.')

    def url(self, name):
        raise ValueError('Free demo has no uploaded-media URLs.')


class RejectUploadHandler(FileUploadHandler):
    def new_file(self, *args, **kwargs):
        raise PermissionDenied('Uploads are disabled in the free demonstration.')


class FreeDemoRestrictions:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        multipart = (request.content_type or '').startswith('multipart/')
        admin_write = (request.path.startswith('/admin/') and request.method not in ('GET', 'HEAD', 'OPTIONS')
                       and request.path not in ('/admin/login/', '/admin/logout/'))
        if multipart or admin_write:
            return JsonResponse({'error': {'code': 'free_demo_read_only',
                'message': 'This demonstration is read-only. Content edits and uploads are disabled.'}}, status=403)
        return self.get_response(request)


@require_safe
def health(request):
    from content.models import TopicPublication
    try:
        TopicPublication.objects.values_list('pk', flat=True).first()
    except DatabaseError:
        return JsonResponse({'status': 'unavailable', 'error': {'code': 'demo_database_unavailable'}},
                            status=503, headers={'Cache-Control': 'no-store'})
    return JsonResponse({'status': 'ok'}, headers={'Cache-Control': 'no-store'})
