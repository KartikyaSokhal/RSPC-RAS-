"""Validate forward migration on a NEW private copy. No original writes or output of records."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys


def old_content(path, columns=None, original_ids=None):
    with sqlite3.connect(f'file:{Path(path).resolve()}?mode=ro', uri=True) as connection:
        assert connection.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert not connection.execute('PRAGMA foreign_key_check').fetchall()
        if columns is None:
            tables = [r[0] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'django_migrations' ORDER BY name")]
            columns = {table: [r[1] for r in connection.execute(f'PRAGMA table_info("{table}")')] for table in tables}
        result = {}; ids = {}
        for table, fields in columns.items():
            selected = ','.join('"' + f.replace('"', '""') + '"' for f in fields)
            rows = connection.execute(f'SELECT {selected} FROM "{table}" ORDER BY 1').fetchall()
            ids[table] = [r[0] for r in rows]
            if original_ids is not None:
                existing = set(original_ids[table])
                if table not in ['auth_permission', 'django_content_type']:
                    assert ids[table] == original_ids[table], f'Unexpected row changes: {table}'
                rows = [r for r in rows if r[0] in existing]
            result[table] = {'rows': len(rows), 'hash': hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode()).hexdigest()}
        return columns, result, ids


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('restored_database'); parser.add_argument('new_directory')
    args = parser.parse_args(); root = Path(args.new_directory).resolve(); root.mkdir(mode=0o700)
    target = root / 'migration-copy.sqlite3'
    with sqlite3.connect(f'file:{Path(args.restored_database).resolve()}?mode=ro', uri=True) as source, sqlite3.connect(target) as destination:
        source.backup(destination)
    target.chmod(0o600)
    columns, before, original_ids = old_content(target)
    with sqlite3.connect(f'file:{target}?mode=ro', uri=True) as connection:
        sequences = dict(connection.execute('SELECT name, seq FROM sqlite_sequence'))
    env = {**os.environ, 'PYTHON_DOTENV_DISABLED': '1', 'DATABASE_PATH': str(target), 'PRIVATE_MEDIA_ROOT': str(root / 'media'), 'AI_ENABLED': 'false', 'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': '', 'DJANGO_ENV': 'development'}
    backend = Path(__file__).resolve().parents[1] / 'backend'
    subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], cwd=backend, env=env, check=True)
    _, after, _ = old_content(target, columns, original_ids)
    assert before == after, 'Original columns or rows changed'
    with sqlite3.connect(f'file:{target}?mode=ro', uri=True) as connection:
        migrated_sequences = dict(connection.execute('SELECT name, seq FROM sqlite_sequence'))
        assert all(migrated_sequences[k] == value for k, value in sequences.items() if k not in ['auth_permission', 'django_content_type', 'django_migrations']), 'Original ID counters changed'
        for table in ['content_topicpublication', 'content_quizreview', 'content_learningresource', 'content_airequest']:
            assert connection.execute(f'SELECT count(*) FROM {table}').fetchone()[0] == 0
    print(json.dumps({'original_tables_preserved': len(before), 'original_rows_preserved': sum(t['rows'] for t in before.values()), 'original_id_counters_preserved': True, 'new_publication_review_resources_empty': True, 'integrity': 'ok', 'foreign_key_errors': 0}))
