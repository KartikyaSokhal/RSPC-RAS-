"""Conservative monetary reservations; no prompts, raw IPs or answers stored."""
from datetime import timedelta
import uuid
from django.conf import settings
from django.db import transaction, OperationalError
from django.db.models import F
from django.utils import timezone
from ..models import AiBudgetBucket, AiRequest
from ..exceptions import ServiceError


def reserve(visitor, ip_key, input_upper_bound):
    now = timezone.now()
    if input_upper_bound > settings.AI_INPUT_TOKEN_LIMIT:
        raise ServiceError('context_too_large', 'Try a shorter question or selection.', 400)
    if min(settings.AI_DAILY_BUDGET_MICRO, settings.AI_INPUT_RATE_MICRO, settings.AI_OUTPUT_RATE_MICRO) <= 0:
        raise ServiceError('ai_unavailable', 'The tutor budget is not configured.', 503)
    cost = (input_upper_bound * settings.AI_INPUT_RATE_MICRO + settings.AI_OUTPUT_TOKEN_LIMIT * settings.AI_OUTPUT_RATE_MICRO + 999999) // 1000000
    day = now.strftime('%Y-%m-%d'); minute = now.strftime('%Y-%m-%dT%H:%M')
    buckets = [(f'global:{day}', None), (f'visitor:{visitor}:{day}', settings.AI_VISITOR_DAILY_LIMIT),
               (f'ip:{ip_key}:{day}', settings.AI_IP_DAILY_LIMIT), (f'minute:{visitor}:{minute}', settings.AI_MINUTE_LIMIT)]
    try:
        with transaction.atomic():
            # Conditional global-row UPDATE serializes contenders on PostgreSQL and SQLite.
            for key, limit in buckets:
                AiBudgetBucket.objects.get_or_create(key=key)
                qs = AiBudgetBucket.objects.filter(key=key)
                if limit is None: qs = qs.filter(reserved_micro__lte=settings.AI_DAILY_BUDGET_MICRO - cost)
                else: qs = qs.filter(requests__lt=limit)
                if not qs.update(reserved_micro=F('reserved_micro') + cost, requests=F('requests') + 1):
                    raise ServiceError('quota_exceeded', 'The tutor limit has been reached. Please continue with the learning materials.', 429)
            if AiRequest.objects.filter(visitor_key=visitor, state='reserved', deadline_at__gt=now).exists():
                raise ServiceError('request_in_progress', 'Please wait for your current response.', 429)
            return AiRequest.objects.create(request_id=uuid.uuid4(), visitor_key=visitor, bucket_keys=[b[0] for b in buckets],
                    reserved_micro=cost, model=settings.AI_MODEL, deadline_at=now + timedelta(seconds=settings.AI_TIMEOUT_SECONDS + 15))
    except OperationalError:
        raise ServiceError('ai_busy', 'The tutor is busy. Please try again later.', 503) from None


def finish(reservation, actual_micro=None):
    # Only known, bounded actual usage can release the unused monetary reservation.
    try:
        with transaction.atomic():
            # PostgreSQL permits concurrent readers; lock before checking completion.
            row = AiRequest.objects.select_for_update().get(pk=reservation.pk)
            if row.state != 'reserved': return
            known = type(actual_micro) is int and 0 <= actual_micro <= row.reserved_micro
            if known:
                AiBudgetBucket.objects.filter(key__in=row.bucket_keys).update(reserved_micro=F('reserved_micro') - (row.reserved_micro - actual_micro))
            row.actual_micro = actual_micro if known else None
            row.state = 'completed' if known else 'ambiguous'
            row.save(update_fields=['actual_micro', 'state'])
    except OperationalError:
        # The original full reservation remains charged. Never retry the provider.
        return
