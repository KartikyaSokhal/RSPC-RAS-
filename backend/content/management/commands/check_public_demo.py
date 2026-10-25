"""Read-only boot gate; never seed, migrate or repair an unexpected target."""
import json
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.db import transaction, connection
from content.services.free_demo_database import HOST, DATABASE
from content.services.public_demo_database import verify_readiness


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            db = connection.settings_dict
            if (connection.vendor != 'postgresql' or db['HOST'] != HOST or db['NAME'] != DATABASE
                    or db['OPTIONS']['sslmode'] != 'verify-full'
                    or not getattr(settings, 'CONTROLLED_DEMO_ONLY', False)):
                raise ValueError('Only the reviewed hosted synthetic profile is eligible.')
            with transaction.atomic():
                with connection.cursor() as c:
                    c.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
                    c.execute('SELECT current_database()=%s,current_user=%s', [db['NAME'],db['USER']])
                    if c.fetchone() != (True, True): raise ValueError('Connection identity mismatch.')
                    c.execute('SHOW server_version_num')
                    if int(c.fetchone()[0]) // 10000 != 17: raise ValueError('PostgreSQL17 required.')
                counts = verify_readiness()
            self.stdout.write(json.dumps({'public_demo_ready': True, 'changed': False, 'counts': counts}))
        except Exception:
            raise CommandError('Public demo boot refused: verify exact target, synthetic account, corpus and runtime grants. No changes performed.') from None
