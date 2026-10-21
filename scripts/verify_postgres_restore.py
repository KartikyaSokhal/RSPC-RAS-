"""Read-only verification of a native PostgreSQL restore against a private rehearsal manifest.

Set explicit POSTGRES_* variables, PREPAL_REHEARSAL_COPY and PRIVATE_MEDIA_ROOT.
The target must be a local prepal_rehearsal_* database; this never performs restore.
"""
import argparse
import json
import os
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    args = parser.parse_args()
    os.environ.update(DJANGO_SETTINGS_MODULE='core.rehearsal_settings', PREPAL_REHEARSAL='1',
                      PYTHON_DOTENV_DISABLED='1', DATABASE_ENGINE='postgresql', DJANGO_ENV='development',
                      AI_ENABLED='false', AI_GUEST_ENABLED='false', GEMINI_API_KEY='', GOOGLE_API_KEY='')
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
    import django
    django.setup()
    from django.db import connections
    from content.services.database_transfer import table_inventory, verify_sequences, assert_disposable_target
    assert_disposable_target(connections['default'])
    expected = json.loads(Path(args.manifest).read_text())['transfer']
    if table_inventory('default') != expected['tables']:
        raise ValueError('Restored records differ from the verified transfer manifest.')
    count = verify_sequences(expected['sequences'])
    connections['default'].check_constraints()
    connections.close_all()
    print(json.dumps({'status': 'PASS', 'tables_compared': len(expected['tables']), 'sequences_verified': count, 'foreign_keys_verified': True, 'records_unchanged': True}))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status': 'FAILED', 'error_type': type(exc).__name__}), file=sys.stderr)
        sys.exit(1)
