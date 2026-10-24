"""Explicit local PG setup/recovery CLI. Reads private files; never prints credentials."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from content.services.postgres_ops import load_environment, provision_local
from content.services import postgres_backup as backups


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    run = sub.add_parser('run-env'); run.add_argument('--env-file', required=True); run.add_argument('argv', nargs=argparse.REMAINDER)
    provision = sub.add_parser('provision-local'); provision.add_argument('--env-file', required=True); provision.add_argument('--database', required=True); provision.add_argument('--new-directory', required=True)
    for operation in ('backup-local', 'restore-local'):
        command = sub.add_parser(operation); command.add_argument('--env-file', required=True); command.add_argument('--pg-bin', required=True); command.add_argument('--openssl', default='openssl')
        if operation == 'backup-local':
            command.add_argument('--media', required=True); command.add_argument('--destination', required=True); command.add_argument('--certificate', required=True)
        else:
            command.add_argument('--database', required=True); command.add_argument('--bundle', required=True); command.add_argument('--private-key', required=True); command.add_argument('--new-directory', required=True)
    health = sub.add_parser('status'); health.add_argument('--directory', required=True); health.add_argument('--maximum-hours', type=int, default=26)
    retention = sub.add_parser('retention-plan'); retention.add_argument('--directory', required=True); retention.add_argument('--days', required=True, type=int)
    args = parser.parse_args()
    if args.command == 'run-env':
        env = load_environment(args.env_file)
        argv = args.argv[1:] if args.argv and args.argv[0] == '--' else args.argv
        if not argv: raise ValueError('Command required.')
        return subprocess.call(argv, env={**os.environ, **env, 'PYTHON_DOTENV_DISABLED': '1'})
    if args.command == 'status':
        result = backups.status(args.directory, args.maximum_hours); print(json.dumps(result)); return 0 if result['healthy'] else 1
    if args.command == 'retention-plan':
        print(json.dumps({'dry_run': True, 'candidates': [p.name for p in backups.retention_candidates(args.directory, args.days)], 'deletion': 'requires owner approval'})); return 0
    env = load_environment(args.env_file)
    if args.command == 'provision-local': result = provision_local(env, args.database, args.new_directory)
    elif args.command == 'backup-local':
        try:
            result = backups.backup(env, args.media, args.destination, args.certificate, args.pg_bin, args.openssl)
        except Exception:
            backups.record_status(args.destination, False); raise
        backups.record_status(args.destination, True)
    else: result = backups.restore_local(env, args.database, args.bundle, args.private_key, args.new_directory, args.pg_bin, args.openssl)
    print(json.dumps(result)); return 0


if __name__ == '__main__':
    try: sys.exit(main())
    except Exception as error:
        print(json.dumps({'status': 'FAILED', 'error_type': type(error).__name__, 'detail': 'No private values emitted; target preserved, inspect configuration.'}), file=sys.stderr)
        sys.exit(1)
