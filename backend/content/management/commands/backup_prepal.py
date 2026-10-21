from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from content.services.backups import backup


class Command(BaseCommand):
    help = 'Create a private backup in a NEW directory. Freeze editorial/media writes first.'

    def add_arguments(self, parser):
        parser.add_argument('destination')

    def handle(self, *args, **options):
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            raise CommandError('This helper backs up isolated SQLite only. Use the documented PostgreSQL pg_dump and restore-verification procedure.')
        try:
            manifest = backup(settings.DATABASES['default']['NAME'], settings.MEDIA_ROOT, options['destination'])
        except (ValueError, OSError) as exc:
            raise CommandError(str(exc)) from None
        self.stdout.write(f"Backup verified: {len(manifest['tables'])} tables, {len(manifest['media'])} media files.")
