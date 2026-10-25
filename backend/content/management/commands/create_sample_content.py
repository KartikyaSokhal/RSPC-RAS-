"""Install original academic sample notes into a fresh, marked demo only."""
import json
from pathlib import Path
import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from content.models import Topic, Tag
from content.services.sample_content import load_corpus, validate_corpus


class Command(BaseCommand):
    help = 'Seed a fresh marked sample demo. Never appends, resets or overwrites data.'

    def handle(self, *args, **options):
        root = Path(getattr(settings, 'DEMO_ROOT', '/invalid')).resolve()
        marker = root / '.sample-demo.json'
        database = settings.DATABASES['default']
        if (not getattr(settings, 'DEMO_MODE', False)
                or database['ENGINE'] != 'django.db.backends.sqlite3'
                or Path(database['NAME']).resolve() != root / 'demo.sqlite3'
                or (root / 'demo.sqlite3').is_symlink()
                or not marker.is_file() or marker.is_symlink()):
            raise CommandError('Refusing sample content outside a new marked isolated demo.')
        try:
            state = json.loads(marker.read_text())
        except (ValueError, OSError) as exc:
            raise CommandError('Invalid sample demo marker.') from exc
        if state != {'kind': 'prepal-academic-sample-v1', 'state': 'preparing'}:
            raise CommandError('Sample demo already prepared or marker invalid; preserving it.')
        if Topic.objects.exists() or get_user_model().objects.exists() or Tag.objects.exists():
            raise CommandError('Database is not empty; refusing to overwrite existing records.')
        corpus, hierarchy = load_corpus()
        validate_corpus(corpus, hierarchy)
        password = secrets.token_urlsafe(24)
        from content.services.sample_install import install_sample
        report, _ = install_sample(password, superuser=True)
        credentials = root / 'admin-credentials.txt'
        with credentials.open('x') as stream:
            stream.write(f'LOCAL SAMPLE ONLY\nUsername: sample-editor\nPassword: {password}\n')
        credentials.chmod(0o600)
        marker.write_text(json.dumps({'kind': 'prepal-academic-sample-v1', 'state': 'ready',
                                     'counts': report}, indent=2))
        self.stdout.write(json.dumps(report, indent=2))
