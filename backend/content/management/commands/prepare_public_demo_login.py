"""Explicit known-database extension. Never run automatically at startup."""
import json
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.db import connection
from content.services.free_demo_database import target
from content.services.postgres_ops import private_file
from content.services.public_demo_database import transition


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--confirm-database', required=True)
        parser.add_argument('--credentials-file', required=True)
        parser.add_argument('--runtime-role', required=True)
        parser.add_argument('--local-test', action='store_true')
        parser.add_argument('--apply', action='store_true')

    def handle(self, *args, **options):
        try:
            import os
            db = connection.settings_dict
            target({'DATABASE_ENGINE': 'postgresql' if connection.vendor == 'postgresql' else 'sqlite',
                    'POSTGRES_HOST': db['HOST'], 'POSTGRES_DB': db['NAME'],
                    'POSTGRES_SSLMODE': db.get('OPTIONS', {}).get('sslmode'),
                    'PREPAL_FREE_DEMO': os.environ.get('PREPAL_FREE_DEMO'),
                    'PREPAL_FREE_DEMO_SYNTHETIC_DATA': os.environ.get('PREPAL_FREE_DEMO_SYNTHETIC_DATA')}, options['local_test'])
            if options['confirm_database'] != db['NAME'] or settings.STUDENT_FEATURES_ENABLED or settings.AI_ENABLED:
                raise ValueError('Use closed operator settings and explicit exact target confirmation.')
            with connection.cursor() as c:
                c.execute('SELECT current_database()=%s,current_user=%s', [db['NAME'], db['USER']])
                if c.fetchone() != (True,True): raise ValueError('Connection identity mismatch.')
            credentials = json.loads(private_file(options['credentials_file']).read_text())
            if set(credentials) != {'username','password'}: raise ValueError('Unexpected credential fields.')
            self.stdout.write(json.dumps(transition(credentials['username'],credentials['password'], apply=options['apply'], runtime_role=options['runtime_role'])))
        except Exception:
            raise CommandError('Controlled-login operation refused/failed; no credentials emitted, transaction rolled back. Verify known synthetic state, private password and limited roles.') from None
