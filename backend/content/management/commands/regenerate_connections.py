from django.core.management.base import BaseCommand, CommandError
from content.services.connections import queue_connections, process_pending
from content.models import ConnectionScan


class Command(BaseCommand):
    help = 'Recheck a bounded batch of published articles. Never auto-approves or rewrites HTML.'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=20)
        parser.add_argument('--all-current', action='store_true', help='Queue existing publications again, preserving decisions.')

    def handle(self, *args, **options):
        if not 1 <= options['limit'] <= 200: raise CommandError('Limit must be between 1 and 200.')
        if options['all_current']: queue_connections()
        processed = process_pending(options['limit'])
        pending = ConnectionScan.objects.filter(pending=True, publication__is_published=True).count()
        self.stdout.write(f'Processed {processed} scans; {pending} remain pending. Review proposals in Admin.')
