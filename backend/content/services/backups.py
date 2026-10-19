"""Private SQLite/media backup. Restore always targets a new directory."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def inventory(database):
    with sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True) as con:
        con.execute('PRAGMA query_only=ON')
        if con.execute('PRAGMA integrity_check').fetchall() != [('ok',)] or con.execute('PRAGMA foreign_key_check').fetchall():
            raise ValueError('Database integrity check failed')
        tables = {}
        for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            quoted = '"' + name.replace('"', '""') + '"'
            rows = sorted(repr(row) for row in con.execute('SELECT * FROM ' + quoted))
            tables[name] = {'count': len(rows), 'sha256': hashlib.sha256('\n'.join(rows).encode()).hexdigest()}
        return tables


def backup(database, media, destination):
    database, media, destination = Path(database).resolve(), Path(media).resolve(), Path(destination).resolve()
    if destination == database.parent or destination == media or media in destination.parents:
        raise ValueError('Backup must be outside database/media directories')
    destination.mkdir(mode=0o700, parents=True, exist_ok=False)
    target = destination / 'database.sqlite3'
    with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as source, sqlite3.connect(target) as copy:
        source.backup(copy)
    os.chmod(target, 0o600)
    files = {}
    if media.exists():
        for path in sorted(media.rglob('*')):
            if path.is_symlink():
                raise ValueError('Media symlinks are not allowed in backups')
            if path.is_file():
                name = path.relative_to(media).as_posix()
                dest = destination / 'media' / name
                dest.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                shutil.copyfile(path, dest)
                os.chmod(dest, 0o600)
                files[name] = digest(dest)
                if files[name] != digest(path):
                    raise ValueError('Media changed during backup; freeze editorial writes and retry')
    manifest = {'format': 1, 'database_sha256': digest(target), 'tables': inventory(target), 'media': files}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    os.chmod(destination / 'manifest.json', 0o600)
    return manifest


def restore(backup_dir, destination):
    backup_dir, destination = Path(backup_dir).resolve(), Path(destination).resolve()
    manifest = json.loads((backup_dir / 'manifest.json').read_text())
    if digest(backup_dir / 'database.sqlite3') != manifest['database_sha256']:
        raise ValueError('Backup checksum mismatch')
    destination.mkdir(parents=True, exist_ok=False, mode=0o700)
    shutil.copyfile(backup_dir / 'database.sqlite3', destination / 'database.sqlite3')
    os.chmod(destination / 'database.sqlite3', 0o600)
    for name, expected in manifest['media'].items():
        source = (backup_dir / 'media' / name).resolve()
        dest = (destination / 'media' / name).resolve()
        if not source.is_relative_to(backup_dir / 'media') or not dest.is_relative_to(destination / 'media'):
            raise ValueError('Invalid media path')
        if digest(source) != expected:
            raise ValueError('Media checksum mismatch')
        dest.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        shutil.copyfile(source, dest)
        os.chmod(dest, 0o600)
    if inventory(destination / 'database.sqlite3') != manifest['tables']:
        raise ValueError('Restored table/primary key/content mismatch')
    return {'tables_verified': len(manifest['tables']), 'media_verified': len(manifest['media'])}
