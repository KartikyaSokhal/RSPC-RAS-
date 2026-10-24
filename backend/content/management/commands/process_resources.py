from django.core.management.base import BaseCommand
from content.models import LearningResource
from content.services.resources import process_resource
from django.db.models import Q
from django.utils import timezone


class Command(BaseCommand):
    help = 'Process bounded pending PDF candidates; no AI or paid OCR.'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10)

    def handle(self, *args, **options):
        eligible = Q(status__in=['pending', 'failed'], attempts__lt=3) | Q(status='processing', processing_deadline__lt=timezone.now())
        ids = list(LearningResource.objects.filter(eligible).order_by('pk').values_list('pk', flat=True)[:max(1, min(options['limit'], 20))])
        count = sum(bool(process_resource(pk)) for pk in ids)
        self.stdout.write(f'Processed {count} candidates. Review page text in Admin before approval.')
