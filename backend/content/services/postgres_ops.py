"""Private local provisioning and native PostgreSQL inventory; no Django setup or cutover."""
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import stat
import uuid
from dotenv import dotenv_values
import psycopg
from psycopg import sql
import datetime
from decimal import Decimal

def canonical(value):
    if isinstance(value, datetime.datetime):
        return value.astimezone(datetime.timezone.utc).isoformat() if value.tzinfo else value.isoformat()
    if isinstance(value, (datetime.date, datetime.time, uuid.UUID, Decimal)): return str(value)
    if isinstance(value, (bytes, memoryview)): return bytes(value).hex()
    raise TypeError("Unsupported backup field type.")


def private_file(path):
    path = Path(path).expanduser()
    if path.is_symlink() or not path.is_file() or (path.stat().st_mode & 0o077 or path.stat().st_uid != os.getuid()):
        raise ValueError('Private input must be a nonsymlink file accessible only by its owner.')
    return path.resolve()


def load_environment(path):
    return {k: v for k, v in dotenv_values(private_file(path)).items() if v is not None}


def write_private(path, data):
    path = Path(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream: stream.write(data)


def connection_options(env, database=None):
    from core.database import database_config
    config = database_config(env, production=env.get('DJANGO_ENV') == 'production')
    if config['ENGINE'] != 'django.db.backends.postgresql': raise ValueError('PostgreSQL required.')
    return {'dbname': database or config['NAME'], 'user': config['USER'], 'password': config['PASSWORD'],
            'host': config['HOST'], 'port': config['PORT'], **config['OPTIONS']}


def local_target(env, name):
    if env.get('POSTGRES_HOST') not in ('127.0.0.1', 'localhost', '::1') or not re.fullmatch(r'prepal_(?:local|rehearsal)_[a-z0-9_]{1,35}', name):
        raise ValueError('Only explicitly named new disposable loopback PostgreSQL targets are supported.')


def grants(connection, runtime, backup):
    with connection.cursor() as cursor:
        cursor.execute('REVOKE ALL ON SCHEMA public FROM PUBLIC')
        for role, rights in ((runtime, sql.SQL('SELECT, INSERT, UPDATE, DELETE')), (backup, sql.SQL('SELECT'))):
            cursor.execute(sql.SQL('GRANT USAGE ON SCHEMA public TO {}').format(sql.Identifier(role)))
            cursor.execute(sql.SQL('GRANT {} ON ALL TABLES IN SCHEMA public TO {}').format(rights, sql.Identifier(role)))
            cursor.execute(sql.SQL('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT {} ON TABLES TO {}').format(rights, sql.Identifier(role)))
        cursor.execute(sql.SQL('GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {}').format(sql.Identifier(runtime)))
        cursor.execute(sql.SQL('GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO {}').format(sql.Identifier(backup)))
        cursor.execute(sql.SQL('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO {}').format(sql.Identifier(runtime)))
        cursor.execute(sql.SQL('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO {}').format(sql.Identifier(backup)))


def provision_local(admin_env, name, directory):
    local_target(admin_env, name)
    if admin_env.get('PREPAL_LOCAL_POSTGRES_SETUP') != '1': raise ValueError('Explicit local provisioning flag required.')
    root = Path(directory).expanduser().absolute()
    if root.exists() or root.is_symlink(): raise ValueError('Provisioning needs a new private output directory.')
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    suffix = uuid.uuid4().hex[:12]
    roles = {kind: f'prepal_{kind}_{suffix}' for kind in ('migration', 'runtime', 'backup')}
    passwords = {kind: secrets.token_urlsafe(40) for kind in roles}
    with psycopg.connect(**connection_options(admin_env, 'postgres'), autocommit=True) as admin:
        if admin.execute('SELECT 1 FROM pg_database WHERE datname=%s', [name]).fetchone(): raise ValueError('Existing target is preserved.')
        # Protect credential-bearing DDL from session statement/error logging.
        admin.execute("SET log_statement='none'")
        admin.execute("SET log_min_error_statement='panic'")
        admin.execute('SET log_min_duration_statement=-1')
        admin.execute('SET log_min_duration_sample=-1')
        admin.execute('SET log_transaction_sample_rate=0')
        for kind, role in roles.items():
            admin.execute(sql.SQL('CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS CONNECTION LIMIT {} PASSWORD {}').format(
                sql.Identifier(role), sql.Literal(10 if kind == 'runtime' else 2), sql.Literal(passwords[kind])))
        admin.execute(sql.SQL('CREATE DATABASE {} OWNER {}').format(sql.Identifier(name), sql.Identifier(roles['migration'])))
        admin.execute(sql.SQL('REVOKE ALL ON DATABASE {} FROM PUBLIC').format(sql.Identifier(name)))
        for role in roles.values(): admin.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO {}').format(sql.Identifier(name), sql.Identifier(role)))
    secret = secrets.token_urlsafe(64)
    for kind, role in roles.items():
        env = {**{k: v for k, v in admin_env.items() if k.startswith('POSTGRES_')},
               'POSTGRES_DB': name, 'POSTGRES_USER': role, 'POSTGRES_PASSWORD': passwords[kind],
               'DATABASE_ENGINE': 'postgresql', 'DJANGO_ENV': 'development', 'SECRET_KEY': secret,
               'PREPAL_LOCAL_POSTGRES': '1', 'PYTHON_DOTENV_DISABLED': '1', 'STUDENT_FEATURES_ENABLED': 'false',
               'AI_ENABLED': 'false', 'AI_GUEST_ENABLED': 'false', 'GOOGLE_CLIENT_ID': '', 'GOOGLE_CLIENT_SECRET': '',
               'GOOGLE_REDIRECT_URI': '', 'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': '',
               'PREPAL_MIGRATION_ROLE': roles['migration'], 'PREPAL_RUNTIME_ROLE': roles['runtime'], 'PREPAL_BACKUP_ROLE': roles['backup']}
        if kind == 'backup': env.pop('SECRET_KEY')  # Native backups never need application signing authority.
        if kind == 'migration': env['POSTGRES_STATEMENT_TIMEOUT_MS'] = '120000'
        write_private(root / f'{kind}.env', ''.join(f'{k}={json.dumps(str(v))}\n' for k, v in sorted(env.items())))
    env = load_environment(root / 'migration.env')
    with psycopg.connect(**connection_options(env)) as migration:
        grants(migration, roles['runtime'], roles['backup'])
    report = {'database': name, 'roles': roles, 'cutover': 'NOT_PERFORMED', 'schema': 'Apply migrations explicitly to this fresh target.'}
    write_private(root / 'provision.json', json.dumps(report, indent=2))
    return report


def inventory(connection):
    """Deterministic hashes of every public table/PK; no private rows leave the process."""
    tables = {}; sequences = {}
    names = connection.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename").fetchall()
    for (table,) in names:
        columns = [r[0] for r in connection.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position", [table])]
        keys = [r[0] for r in connection.execute("SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=ANY(i.indkey) WHERE i.indrelid=%s::regclass AND i.indisprimary ORDER BY a.attnum", ['public.' + table])]
        if not keys: raise ValueError('All backed-up application tables must have primary keys.')
        query = sql.SQL('SELECT {} FROM {} ORDER BY {}').format(sql.SQL(',').join(map(sql.Identifier, columns)), sql.Identifier('public', table), sql.SQL(',').join(map(sql.Identifier, keys)))
        count = 0; digest = hashlib.sha256()
        with connection.cursor(name='backup_' + uuid.uuid4().hex) as cursor:
            cursor.execute(query)
            for row in cursor:
                digest.update(json.dumps(row, default=canonical, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode() + b'\n'); count += 1
        tables[table] = {'count': count, 'sha256': digest.hexdigest(), 'columns': columns}
    for (name,) in connection.execute("SELECT sequencename FROM pg_sequences WHERE schemaname='public' ORDER BY sequencename"):
        row = connection.execute(sql.SQL('SELECT last_value,is_called FROM {}').format(sql.Identifier('public', name))).fetchone()
        sequences[name] = list(row)
    return {'tables': tables, 'sequences': sequences}


def verify_inventory(actual, expected):
    if actual['tables'] != expected['tables']: raise ValueError('Restored tables/fields/IDs differ from the backup snapshot.')
    if set(actual['sequences']) != set(expected['sequences']): raise ValueError('Restored sequences differ.')
    for name, (value, called) in expected['sequences'].items():
        restored, restored_called = actual['sequences'][name]
        if restored < value or (called and not restored_called): raise ValueError('A restored sequence could reuse historical IDs.')
    return {'tables_verified': len(actual['tables']), 'rows_verified': sum(t['count'] for t in actual['tables'].values()), 'sequences_verified': len(actual['sequences'])}
