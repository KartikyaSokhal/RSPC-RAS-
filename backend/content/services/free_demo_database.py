"""Narrow existing-database operations. Secrets are files, never command arguments/output."""
import hashlib
import json
from pathlib import Path
import re
import secrets
import tempfile
import tarfile
import psycopg
from psycopg import sql
from .postgres_ops import load_environment, write_private

HOST = 'dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com'
DATABASE = 'prepal_staging_db'
MARKER = 'prepal_free_demo_manifest'


def target(env, local=False):
    host, name = env.get('POSTGRES_HOST'), env.get('POSTGRES_DB')
    if local:
        if host != '127.0.0.1' or not re.fullmatch(r'prepal_free_demo_test_[a-z0-9_]{1,32}', name or ''):
            raise ValueError('Local rehearsal requires loopback and a new prepal_free_demo_test_* target.')
    elif host != HOST or name != DATABASE or env.get('POSTGRES_SSLMODE') != 'verify-full':
        raise ValueError('Only the approved Render database with external verify-full TLS is eligible.')
    if env.get('PREPAL_FREE_DEMO') != '1' or env.get('PREPAL_FREE_DEMO_SYNTHETIC_DATA') != '1':
        raise ValueError('Both explicit synthetic free-demo confirmations are required.')
    if env.get('DATABASE_ENGINE') != 'postgresql':
        raise ValueError('PostgreSQL is mandatory; no SQLite fallback.')


def connect(env, local=False, readonly=False):
    target(env, local)
    import certifi
    ca = env.get('POSTGRES_SSLROOTCERT') or certifi.where()
    options = '-c statement_timeout=120000 -c lock_timeout=5000 -c idle_in_transaction_session_timeout=120000'
    if readonly: options += ' -c default_transaction_read_only=on'
    args = dict(host=env['POSTGRES_HOST'], port=env.get('POSTGRES_PORT', '5432'),
                dbname=env['POSTGRES_DB'], user=env['POSTGRES_USER'], password=env['POSTGRES_PASSWORD'],
                sslmode=env.get('POSTGRES_SSLMODE', 'disable'), connect_timeout=15, options=options)
    if not local: args['sslrootcert'] = ca
    return psycopg.connect(**args)


def identity(conn, env):
    row = conn.execute('SELECT current_database()=%s,current_user=%s', (env['POSTGRES_DB'], env['POSTGRES_USER'])).fetchone()
    if row != (True, True): raise ValueError('Connection identity does not match the private configuration.')


def objects(conn):
    return conn.execute("SELECT c.relname,c.relkind FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind IN ('r','p','v','m','S','f') ORDER BY c.relname").fetchall()


def require_empty(conn):
    if objects(conn): raise ValueError('Target is not empty; unknown or existing data is preserved.')
    if conn.execute("SELECT count(*) FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname NOT IN ('public','information_schema')").fetchone()[0]:
        raise ValueError('Unknown schema is preserved.')
    if conn.execute("SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname<>'information_schema'").fetchone()[0]:
        raise ValueError('Unknown routines are preserved.')
    if conn.execute('SELECT count(*) FROM pg_largeobject_metadata').fetchone()[0]:
        raise ValueError('Existing large objects are preserved.')
    if conn.execute("SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='public' AND t.typtype IN ('d','e')").fetchone()[0]:
        raise ValueError('Unknown database types are preserved.')


def prepare(config, directory, local=False):
    env = load_environment(config)
    # Original internal-host file is preserved; use only its already approved external peer.
    if not local and env.get('POSTGRES_HOST') == HOST.split('.')[0]: env['POSTGRES_HOST'] = HOST
    env.update(DATABASE_ENGINE='postgresql', PREPAL_FREE_DEMO='1', PREPAL_FREE_DEMO_SYNTHETIC_DATA='1')
    target(env, local)
    requested=Path(directory).expanduser()
    root=requested.resolve()
    app=Path(__file__).resolve().parents[3]
    if requested.exists() or requested.is_symlink() or root.is_relative_to(app):
        raise ValueError('Preparation requires a NEW private directory outside application source.')
    with connect(env, local, readonly=True) as conn:
        identity(conn, env); require_empty(conn)
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    env.update(PYTHON_DOTENV_DISABLED='1', DJANGO_ENV='production' if not local else 'development',
               DEBUG='false', PREPAL_ENVIRONMENT='free-demo', SECRET_KEY=secrets.token_urlsafe(64),
               STAGING_ACCESS_USERNAME='synthetic-operator', STAGING_ACCESS_PASSWORD=secrets.token_urlsafe(32),
               ALLOWED_HOSTS='rspc-ras.onrender.com' if not local else '127.0.0.1,testserver',
               SITE_ORIGIN='https://rspc-ras.onrender.com' if not local else 'https://127.0.0.1',
               STUDENT_FEATURES_ENABLED='false', AI_ENABLED='false', AI_GUEST_ENABLED='false',
               GEMINI_API_KEY='', GOOGLE_API_KEY='', GOOGLE_CLIENT_ID='', GOOGLE_CLIENT_SECRET='',
               PREPAL_FREE_DEMO_LOCAL_TEST='1' if local else '0')
    roles = {'migration': 'prepal_demo_migration', 'runtime': 'prepal_demo_runtime'}
    if local:
        suffix = secrets.token_hex(4)
        roles = {k:v+'_'+suffix for k,v in roles.items()}
    for kind, role in roles.items():
        data = env | {'POSTGRES_USER':role,'POSTGRES_PASSWORD':secrets.token_urlsafe(40)}
        write_private(root/(kind+'.env'), ''.join(k+'='+json.dumps(str(v))+'\n' for k,v in sorted(data.items())))
    write_private(root/'staff-password.txt', secrets.token_urlsafe(32)+'\n')
    write_private(root/'plan.json',json.dumps({'host':env['POSTGRES_HOST'],'database':env['POSTGRES_DB'],'roles':roles,'local':local}))
    return {'prepared':True,'live_schema_or_data_changed':False}


def role_flags(conn, name):
    row = conn.execute('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls FROM pg_roles WHERE rolname=%s',(name,)).fetchone()
    return row


def apply_roles(config, directory, local=False):
    env=load_environment(config)
    if not local and env.get('POSTGRES_HOST') == HOST.split('.')[0]: env['POSTGRES_HOST']=HOST
    env.update(DATABASE_ENGINE='postgresql',PREPAL_FREE_DEMO='1',PREPAL_FREE_DEMO_SYNTHETIC_DATA='1')
    configs={k:load_environment(Path(directory)/(k+'.env')) for k in ('migration','runtime')}
    for value in configs.values():
        target(value,local)
        if any(value[k]!=env[k] for k in ('POSTGRES_HOST','POSTGRES_DB','POSTGRES_PORT')): raise ValueError('Prepared role target mismatch.')
    with connect(env,local) as conn:
        identity(conn,env); require_empty(conn)
        for value in configs.values():
            role=value['POSTGRES_USER']
            if role_flags(conn,role) is not None: raise ValueError('Existing role preserved; verify prepared credentials instead of resetting it.')
            # SCRAM verifier avoids submitting plaintext passwords in credential-bearing DDL.
            verifier=conn.pgconn.encrypt_password(value['POSTGRES_PASSWORD'].encode(),role.encode(),b'scram-sha-256').decode()
            conn.execute(sql.SQL('CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS CONNECTION LIMIT 4 PASSWORD {}').format(sql.Identifier(role),sql.Literal(verifier)))
            conn.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO {}').format(sql.Identifier(env['POSTGRES_DB']),sql.Identifier(role)))
        conn.execute(sql.SQL('REVOKE TEMPORARY ON DATABASE {} FROM PUBLIC').format(sql.Identifier(env['POSTGRES_DB'])))
        conn.execute('REVOKE CREATE ON SCHEMA public FROM PUBLIC')
        conn.execute(sql.SQL('GRANT USAGE,CREATE ON SCHEMA public TO {}').format(sql.Identifier(configs['migration']['POSTGRES_USER'])))
        conn.execute(sql.SQL('GRANT USAGE ON SCHEMA public TO {}').format(sql.Identifier(configs['runtime']['POSTGRES_USER'])))
    return {'roles_created':2,'database_schema_initialized':False}


def grant_runtime(directory, local=False):
    migration=load_environment(Path(directory)/'migration.env');runtime=load_environment(Path(directory)/'runtime.env')
    target(runtime,local)
    if any(migration[k]!=runtime[k] for k in ('POSTGRES_HOST','POSTGRES_PORT','POSTGRES_DB')):raise ValueError('Runtime/migration identity mismatch.')
    with connect(migration,local) as conn:
        identity(conn,migration)
        if role_flags(conn,runtime['POSTGRES_USER'])!=(False,False,False,False,False):raise ValueError('Unsafe runtime role flags.')
        if conn.execute('SELECT count(*) FROM pg_auth_members m JOIN pg_roles r ON r.oid=m.member WHERE r.rolname=%s',(runtime['POSTGRES_USER'],)).fetchone()[0]:raise ValueError('Runtime privileged membership is forbidden.')
        if (MARKER,'r') not in objects(conn): raise ValueError('Verified initialization marker required before grants.')
        role=sql.Identifier(runtime['POSTGRES_USER'])
        conn.execute(sql.SQL('GRANT SELECT ON ALL TABLES IN SCHEMA public TO {}').format(role))
        conn.execute(sql.SQL('GRANT INSERT,UPDATE,DELETE ON django_session TO {}').format(role))
        conn.execute(sql.SQL('GRANT UPDATE(last_login,password) ON auth_user TO {}').format(role))
    return {'runtime_grants':'content/framework SELECT; session CRUD; auth last_login/password bookkeeping'}


def corpus_digest():
    root=Path(__file__).resolve().parents[1]/'fixtures'
    return hashlib.sha256(b''.join((root/n).read_bytes() for n in ('syllabus_142.json','sample_lessons_v1.json'))).hexdigest()


def create_backup(config,destination,certificate,bindir,openssl='openssl',local=False):
    """Read-only snapshot to a NEW encrypted local bundle; no scheduler/remote restore."""
    from .postgres_backup import native_env,run,tool,digest,media_inventory
    from .postgres_ops import inventory
    import certifi
    env=load_environment(config);target(env,local)
    if not local:env['POSTGRES_SSLROOTCERT']=env.get('POSTGRES_SSLROOTCERT') or certifi.where()
    requested=Path(destination).expanduser()
    root=requested.resolve()
    app=Path(__file__).resolve().parents[3]
    if requested.exists() or requested.is_symlink() or root.is_relative_to(app):raise ValueError('Backup needs a NEW private path outside application source.')
    certificate=Path(certificate).resolve(strict=True)
    version=run([tool(bindir,'pg_dump'),'--version']).decode()
    match=re.search(r'(\d+)\.',version)
    with connect(env,local,readonly=True) as conn:
        conn.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
        identity(conn,env)
        if not match or int(match[1])<conn.info.server_version//10000:raise ValueError('Native pg_dump must support the server major version.')
        if (MARKER,'r') not in objects(conn):raise ValueError('Verified demo marker required for backup.')
        meta=conn.execute('SELECT metadata FROM '+MARKER+' WHERE id=1').fetchone()[0]
        if meta!={'version':1,'database':env['POSTGRES_DB'],'corpus':corpus_digest()}:raise ValueError('Backup target marker mismatch.')
        if conn.execute('SELECT count(*) FROM content_learningresource').fetchone()[0]:raise ValueError('Free-demo backups refuse uploaded resources.')
        snapshot=conn.execute('SELECT pg_export_snapshot()').fetchone()[0]
        manifest=inventory(conn)
        root.mkdir(mode=0o700,parents=True,exist_ok=False)
        with tempfile.TemporaryDirectory(prefix='.snapshot-',dir=root) as temporary:
            stage=Path(temporary);(stage/'media').mkdir(mode=0o700)
            args=native_env(env);args['PGOPTIONS']+=' -c default_transaction_read_only=on'
            run([tool(bindir,'pg_dump'),'--format=custom','--no-owner','--no-acl','--schema=public','--snapshot='+snapshot,'--lock-wait-timeout=5s','--file='+str(stage/'database.dump')],env=args)
            manifest.update(format=1,media=media_inventory(stage/'media'),dump_sha256=digest(stage/'database.dump'))
            write_private(stage/'manifest.json',json.dumps(manifest,sort_keys=True))
            with tarfile.open(stage/'bundle.tar','w') as archive:
                for name in ('database.dump','manifest.json','media'):archive.add(stage/name,arcname=name)
            output=root/'snapshot.cms'
            run([openssl,'cms','-encrypt','-binary','-aes-256-gcm','-outform','DER','-in',str(stage/'bundle.tar'),'-out',str(output),str(certificate)])
            output.chmod(0o600)
    receipt={'format':'CMS-AES-256-GCM','sha256':digest(output),'tables':len(manifest['tables']),
             'rows':sum(t['count'] for t in manifest['tables'].values()),'uploads':0,'native_version':version.strip()}
    write_private(root/'receipt.json',json.dumps(receipt,indent=2));return receipt
