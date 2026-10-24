"""Local native PG recovery drills. CMS AES-GCM authenticates encrypted DB+media bundles.

No production execution or off-host transfer is enabled here. Production requires
an approved destination, schedule, monitoring and retention policy first.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import uuid

import psycopg
from .postgres_ops import (connection_options, grants, inventory, load_environment,
                           local_target, private_file, provision_local, verify_inventory, write_private)


def digest(path):
    with Path(path).open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()


def native_env(env):
    config = connection_options(env)
    # Do not inherit connection/service overrides or a credential-bearing connection URI.
    result = {k: v for k, v in os.environ.items() if not k.startswith(('PG', 'POSTGRES_'))}
    result.update(PGDATABASE=config['dbname'], PGUSER=config['user'], PGPASSWORD=config['password'],
                  PGHOST=config['host'], PGPORT=str(config['port']), PGSSLMODE=config['sslmode'],
                  PGCONNECT_TIMEOUT=str(config['connect_timeout']), PGOPTIONS=config['options'])
    if config.get('sslrootcert'): result['PGSSLROOTCERT'] = config['sslrootcert']
    return result


def tool(bindir, name):
    path = Path(bindir).resolve() / name
    if not path.is_file(): raise ValueError('Explicit native PostgreSQL bin directory required.')
    return str(path)


def run(argv, **kwargs):
    result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    if result.returncode: raise ValueError('Native backup/encryption operation failed; no credentials emitted.')
    return result.stdout


def media_inventory(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir(): raise ValueError('Explicit nonsymlink private media directory required.')
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or (not path.is_dir() and not path.is_file()): raise ValueError('Unsafe media entry.')
        if path.is_file(): result[path.relative_to(root).as_posix()] = digest(path)
    return result


def private_directory(path):
    path = Path(path).expanduser().absolute()
    if path.is_symlink(): raise ValueError('Private directory cannot be a symlink.')
    path.mkdir(parents=True, mode=0o700, exist_ok=True)
    if path.stat().st_mode & 0o077 or path.stat().st_uid != os.getuid(): raise ValueError('Directory must be private and owned by current user.')
    return path.resolve()


def backup(env, media, destination, certificate, bindir, openssl='openssl'):
    local_target(env, env['POSTGRES_DB'])
    if env.get('DJANGO_ENV') == 'production': raise ValueError('Production backup activation needs approval.')
    destination = private_directory(destination)
    # Never create archives inside application source, public assets or private media itself.
    app = Path(__file__).resolve().parents[3]
    if destination.is_relative_to(app) or destination.is_relative_to(Path(media).resolve()):
        raise ValueError('Backups must be outside application and media directories.')
    before = media_inventory(media)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    name = f'prepal-{stamp}-{uuid.uuid4().hex}.cms'
    output = destination / name
    with tempfile.TemporaryDirectory(prefix='.backup-', dir=destination) as temporary:
        stage = Path(temporary)
        with psycopg.connect(**connection_options(env)) as connection:
            connection.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
            snapshot = connection.execute('SELECT pg_export_snapshot()').fetchone()[0]
            manifest = inventory(connection)
            run([tool(bindir, 'pg_dump'), '--format=custom', '--no-owner', '--no-privileges', '--schema=public',
                 '--snapshot=' + snapshot, '--lock-wait-timeout=5s', '--file=' + str(stage / 'database.dump')], env=native_env(env))
        shutil.copytree(media, stage / 'media')
        if before != media_inventory(media) or before != media_inventory(stage / 'media'):
            raise ValueError('Media changed during backup; retry during an upload freeze.')
        manifest.update(format=1, created_at=stamp, media=before, dump_sha256=digest(stage / 'database.dump'))
        write_private(stage / 'manifest.json', json.dumps(manifest, sort_keys=True))
        with tarfile.open(stage / 'bundle.tar', 'w') as archive:
            for item in ('database.dump', 'manifest.json', 'media'): archive.add(stage / item, arcname=item)
        run([openssl, 'cms', '-encrypt', '-binary', '-aes-256-gcm', '-outform', 'DER',
             '-in', str(stage / 'bundle.tar'), '-out', str(stage / 'encrypted'), str(Path(certificate).resolve(strict=True))])
        os.chmod(stage / 'encrypted', 0o600)
        os.rename(stage / 'encrypted', output)
    receipt = {'file': name, 'sha256': digest(output), 'created_at': stamp, 'format': 'CMS-AES-256-GCM', 'status': 'success'}
    write_private(output.with_suffix('.json'), json.dumps(receipt))
    return receipt


def extract(bundle, private_key, directory, openssl='openssl'):
    bundle, key = private_file(bundle), private_file(private_key)
    root = Path(directory)
    root.mkdir(mode=0o700, exist_ok=False)
    try:
        structure = run([openssl, 'cms', '-cmsout', '-print', '-inform', 'DER', '-in', str(bundle)])
        if b'id-smime-ct-authEnvelopedData' not in structure or b'aes-256-gcm' not in structure:
            raise ValueError('Only authenticated AES-256-GCM CMS bundles are accepted.')
        # AEAD must succeed fully BEFORE inspecting or extracting any plaintext archive.
        run([openssl, 'cms', '-decrypt', '-binary', '-inform', 'DER', '-in', str(bundle),
             '-inkey', str(key), '-out', str(root / 'bundle.tar')])
        os.chmod(root / 'bundle.tar', 0o600)
        with tarfile.open(root / 'bundle.tar') as archive:
            members = archive.getmembers(); names = set()
            for member in members:
                path = Path(member.name)
                if (member.name in names or path.is_absolute() or '..' in path.parts or not path.parts
                        or path.parts[0] not in ('database.dump', 'manifest.json', 'media')
                        or not (member.isfile() or member.isdir())): raise ValueError('Unsafe backup archive.')
                names.add(member.name)
            archive.extractall(root, members=members, filter='data')
        (root / 'bundle.tar').unlink()
        manifest = json.loads((root / 'manifest.json').read_text())
        if (manifest['format'] != 1 or digest(root / 'database.dump') != manifest['dump_sha256']
                or media_inventory(root / 'media') != manifest['media']): raise ValueError('Backup integrity mismatch.')
        return manifest
    except Exception:
        # Only this newly created extraction directory is eligible for cleanup.
        shutil.rmtree(root)
        raise


def restore_local(admin_env, name, bundle, private_key, new_directory, bindir, openssl='openssl'):
    local_target(admin_env, name)
    root = Path(new_directory)
    if root.exists() or root.is_symlink(): raise ValueError('Restore needs a new private directory.')
    root.mkdir(mode=0o700, parents=True)
    manifest = extract(bundle, private_key, root / 'extracted', openssl)
    roles = provision_local(admin_env, name, root / 'credentials')
    env = load_environment(root / 'credentials/migration.env')
    # New databases already contain public. Omit only its CREATE entry, retaining
    # schema ownership/default privileges established by provision_local.
    entries = run([tool(bindir, 'pg_restore'), '--list', str(root / 'extracted/database.dump')])
    filtered = b'\n'.join(line for line in entries.splitlines() if b' SCHEMA - public ' not in line) + b'\n'
    write_private(root / 'restore-list.txt', filtered.decode())
    run([tool(bindir, 'pg_restore'), '--no-owner', '--no-privileges', '--exit-on-error', '--single-transaction',
         '--use-list=' + str(root / 'restore-list.txt'), '--dbname=' + name, str(root / 'extracted/database.dump')], env=native_env(env))
    with psycopg.connect(**connection_options(env)) as connection:
        grants(connection, roles['roles']['runtime'], roles['roles']['backup'])
        actual = inventory(connection)
        result = verify_inventory(actual, manifest)
        if connection.execute("SELECT count(*) FROM pg_constraint WHERE contype='f' AND NOT convalidated").fetchone()[0]:
            raise ValueError('Restored FK constraints are not validated.')
    result['cutover'] = 'NOT_PERFORMED'
    write_private(root / 'verified.json', json.dumps(result))
    return result


def status(directory, maximum_hours=26):
    path = Path(directory) / 'status.json'
    if not path.is_file(): return {'healthy': False, 'code': 'no_backup_status'}
    data = json.loads(private_file(path).read_text())
    age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(data['checked_at'])).total_seconds() / 3600
    return {'healthy': data.get('status') == 'success' and age <= maximum_hours, 'status': data.get('status'), 'age_hours': round(age, 2)}


def record_status(directory, success):
    root = private_directory(directory)
    payload = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'success' if success else 'failed'}
    pending = root / ('.status-' + uuid.uuid4().hex)
    write_private(pending, json.dumps(payload)); os.replace(pending, root / 'status.json')


def retention_candidates(directory, days):
    if not 1 <= days <= 3650: raise ValueError('Retention must be 1–3650 days.')
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    result = []
    for receipt in Path(directory).glob('prepal-*.json'):
        try:
            data = json.loads(private_file(receipt).read_text())
            bundle = Path(directory) / data['file']
            if (Path(data['file']).name != data['file'] or bundle.suffix != '.cms'
                    or receipt != bundle.with_suffix('.json') or data.get('status') != 'success'): continue
            private_file(bundle)
            created = datetime.datetime.strptime(data['created_at'], '%Y%m%dT%H%M%SZ').replace(tzinfo=datetime.timezone.utc)
            if created < cutoff and digest(bundle) == data['sha256']: result.append(bundle)
        except (ValueError, KeyError, OSError): continue
    return result
