"""Prepare a NEW loopback PostgreSQL synthetic preview; never selects a hosted DB."""
import argparse
import json
import os
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True, help='NEW private directory; existing destinations are refused.')
    args = parser.parse_args()
    destination = args.directory.expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        parser.error('Existing destinations are preserved. Choose a NEW directory.')
    if os.environ.get('RENDER') or os.environ.get('PREPAL_PUBLIC_DEMO') != '1':
        parser.error('Explicit local public-demo confirmation required; Render is forbidden.')
    os.environ['PYTHON_DOTENV_DISABLED'] = '1'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.local_postgres_settings'
    sys.path.insert(0, str(ROOT / 'backend'))
    import django
    django.setup()
    from django.db import connection, transaction
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    from content.models import StudentIdentity
    from content.services.sample_install import install_sample
    config = connection.settings_dict
    if not config['NAME'].startswith('prepal_local_public_demo_'):
        parser.error('Only a NEW prepal_local_public_demo_* database is allowed.')
    # Includes objects outside public; never migrate/adopt an existing database.
    with connection.cursor() as cursor:
        cursor.execute('SELECT pg_try_advisory_lock(hashtext(%s))', ['prepal-public-demo:'+config['NAME']])
        if not cursor.fetchone()[0]:
            parser.error('Another preparer is active; no writes performed.')
        cursor.execute("""SELECT current_database(),
            EXISTS(SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema')
            OR EXISTS(SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema')
            OR EXISTS(SELECT 1 FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname NOT IN ('public','information_schema'))""")
        name, populated = cursor.fetchone()
    if name != config['NAME'] or populated:
        parser.error('Database identity mismatch or nonempty database; no writes performed.')
    destination.mkdir(mode=0o700, parents=True, exist_ok=False)
    destination = destination.resolve()
    # No reset/retry after a partial migration; preserve failures for inspection.
    call_command('migrate', interactive=False, verbosity=0)
    accounts = {}
    with transaction.atomic():
        password = secrets.token_urlsafe(24)
        report, _ = install_sample(password, superuser=False)
        accounts['sample-editor'] = password
        for username in ('demo-reader', 'demo-other'):
            password = secrets.token_urlsafe(24)
            email = username + '@example.invalid'
            user = get_user_model().objects.create_user(username, email=email, password=password)
            StudentIdentity.objects.create(user=user, email=email)
            accounts[username] = password
    with open(destination / 'accounts.json', 'x', opener=lambda p, flags: os.open(p, flags, 0o600)) as stream:
        json.dump(accounts, stream)
    marker = {'kind': 'prepal-local-public-demo-v1', 'state': 'ready', 'database': name}
    (destination / '.public-demo.json').write_text(json.dumps(marker))
    (destination / '.public-demo.json').chmod(0o600)
    print(f'NEW local synthetic preview ready: {destination}. 2 synthetic students, 1 view-only staff; {report["topics"] if "topics" in report else 142} topics. Private accounts.json contains credentials; never publish it.')


if __name__ == '__main__':
    main()
