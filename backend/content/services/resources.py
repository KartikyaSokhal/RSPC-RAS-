import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tempfile
from datetime import timedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from ..models import LearningResource, ResourcePage
from ..exceptions import ServiceError
from .publication import visible_publications


def file_digest(resource):
    result = hashlib.sha256()
    with resource.file.open('rb') as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b''): result.update(chunk)
    return result.hexdigest()


def process_resource(resource_id):
    now = timezone.now()
    # Recover stale claims with bounded attempts; approved records are never claimed.
    LearningResource.objects.filter(pk=resource_id, status='processing', processing_deadline__lt=now, attempts__gte=3).update(status='failed', error_code='attempt_limit', processing_deadline=None)
    LearningResource.objects.filter(pk=resource_id, status='processing', processing_deadline__lt=now, attempts__lt=3).update(status='pending')
    with transaction.atomic():
        from django.db.models import F
        claimed = LearningResource.objects.filter(pk=resource_id, status__in=['pending', 'failed'], attempts__lt=3).update(
            status='processing', processing_deadline=now + timedelta(seconds=settings.PDF_TIMEOUT_SECONDS + 10), attempts=F('attempts') + 1)
    if not claimed: return False
    resource = LearningResource.objects.get(pk=resource_id)
    byte_count = 0
    try:
        byte_count = resource.file.size
        if byte_count > settings.PDF_MAX_BYTES: raise ValueError('too_large')
        digest = file_digest(resource)
        with tempfile.TemporaryFile() as output:
            process = subprocess.Popen([sys.executable, '-I', str(Path(__file__).with_name('pdf_extract.py')), resource.file.path, str(settings.PDF_MAX_PAGES)],
                                       stdout=output, stderr=subprocess.DEVNULL, env={'PATH': os.defpath, 'PYTHON_DOTENV_DISABLED': '1'})
            started = time.monotonic()
            try:
                while process.poll() is None:
                    if time.monotonic() - started > settings.PDF_TIMEOUT_SECONDS: raise ValueError('parser_timeout')
                    if sys.platform == 'darwin':
                        monitor = subprocess.run(['/bin/ps', '-o', 'rss=', '-p', str(process.pid)], capture_output=True, timeout=2)
                        if monitor.returncode and process.poll() is None: raise ValueError('memory_monitor_unavailable')
                        rss = monitor.stdout.strip()
                        if rss and int(rss) > 512 * 1024: raise ValueError('parser_memory_limit')
                    time.sleep(0.05)
            finally:
                if process.poll() is None: process.kill()
                process.wait(timeout=5)
            output.seek(0); raw = output.read(12 * 1024 * 1024 + 1)
            if len(raw) > 12 * 1024 * 1024: raise ValueError('output_limit')
            payload = json.loads(raw)
        if file_digest(resource) != digest: raise ValueError('changed_file')
    except (ValueError, OSError, subprocess.TimeoutExpired):
        payload = {'status': 'failed', 'error': 'extraction_failed'}; digest = ''
    with transaction.atomic():
        current = LearningResource.objects.get(pk=resource_id)
        if current.status != 'processing' or current.attempts != resource.attempts: return False
        ResourcePage.objects.filter(resource=current).delete()  # Unpublished candidate pages only.
        for page in payload.get('pages', []): ResourcePage.objects.create(resource=current, **page)
        current.status = payload.get('status', 'failed'); current.error_code = payload.get('error', '')
        current.page_count = len(payload.get('pages', [])); current.sha256 = digest
        current.byte_count = byte_count; current.processing_deadline = None
        current.save()
    return True


def approve_resource(resource, reviewer):
    if resource.status != 'ready' or not resource.rights_note.strip() or not resource.source_reference.strip():
        raise ServiceError('resource_not_ready', 'Review extraction, sources and rights before approval.')
    if not resource.pages.exists() or file_digest(resource) != resource.sha256:
        raise ServiceError('resource_changed', 'The source has changed; upload a new candidate.')
    resource.status = 'approved'; resource.reviewed_by = reviewer; resource.reviewed_at = timezone.now()
    resource.save(update_fields=['status', 'reviewed_by', 'reviewed_at'])


def authorized_resource(resource_id):
    resource = LearningResource.objects.filter(pk=resource_id, status='approved').first()
    pubs = visible_publications()
    pub = pubs.get(resource.topic_id) if resource else None
    if not pub or resource.pk not in pub.snapshot.get('resource_ids', []):
        raise ServiceError('resource_unavailable', 'This resource is not currently available.', 404)
    return resource, pub
