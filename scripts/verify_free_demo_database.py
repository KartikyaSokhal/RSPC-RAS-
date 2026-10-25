"""Reproduce only on NEW disposable loopback PostgreSQL DBs; no hosted execution."""
import argparse
import base64
import hashlib
import json
import os
import re
from pathlib import Path
import secrets
import subprocess
import sys
import uuid
from urllib.parse import urlencode

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from content.services.free_demo_database import connect,target,objects,create_backup
from content.services.postgres_ops import load_environment,write_private,inventory,verify_inventory,connection_options
import psycopg
from psycopg import sql


def worker(kind,config,directory):
    cfg=load_environment(config);target(cfg,True)
    os.environ.update(cfg,PYTHON_DOTENV_DISABLED='1',DJANGO_SETTINGS_MODULE='core.free_demo_ops_settings')
    import django
    django.setup()
    if kind in ('public-fault','public-http','public-refusals'):
        from django.test import Client, override_settings
        from django.db import transaction
        from django.contrib.auth import get_user_model
        from unittest.mock import patch
        from content.services.public_demo_database import transition,verify_runtime,verify_readiness
        from content.management.commands.initialize_free_demo import verify_install
        from content.models import StudentIdentity,Bookmark,Topic
        credentials=json.loads((directory/'student-credentials.json').read_text());username=credentials['username'];password=credentials['password']
        if kind=='public-fault':
            runtime=load_environment(directory/'runtime.env')['POSTGRES_USER']
            with patch('content.services.public_demo_database.verify_runtime',side_effect=ValueError('Synthetic injected failure')):
                try:transition(username,password,apply=True,runtime_role=runtime)
                except ValueError:pass
                else:raise AssertionError('Expected rollback failure.')
            assert get_user_model().objects.count()==1 and not StudentIdentity.objects.exists()
            verify_install()
            return {'controlled_account_and_grants_transactional_rollback':True}
        if kind=='public-refusals':
            try:transition(username,'wrong-synthetic-password-that-is-never-a-credential',apply=True)
            except ValueError:pass
            else:raise AssertionError('Existing password was reset.')
            with transaction.atomic():
                row=Bookmark.objects.create(topic=Topic.objects.first())
                try:transition(username,password,apply=True)
                except ValueError:pass
                else:raise AssertionError('Unknown ownerless data accepted.')
                assert Bookmark.objects.filter(pk=row.pk).exists()
                transaction.set_rollback(True)
            verify_install(public_demo=True)
            return {'controlled_wrong_password_and_unknown_learner_data_refused':True}
        middleware=[m for m in __import__('django.conf',fromlist=['settings']).settings.MIDDLEWARE if not m.endswith('StagingAccessMiddleware')]
        middleware.append('core.public_demo_support.StudentLearningAccessMiddleware')
        with override_settings(STUDENT_FEATURES_ENABLED=True,LEARNING_AUTH_REQUIRED=True,
                CONTROLLED_DEMO_ONLY=True,STUDENT_REGISTRATION_ENABLED=False,
                PASSWORD_RESET_ENABLED=False,MIDDLEWARE=middleware,SESSION_COOKIE_SECURE=True,CSRF_COOKIE_SECURE=True):
            client=Client(enforce_csrf_checks=True)
            response=client.get('/api/config/',secure=True);assert response.status_code==200 and 'WWW-Authenticate' not in response
            assert client.get('/api/topics/',secure=True).status_code==401
            def post(path,data):
                token=client.get('/api/config/',secure=True).json()['csrf_token']
                return client.post(path,data,content_type='application/json',secure=True,HTTP_X_CSRFTOKEN=token,HTTP_ORIGIN='https://testserver')
            assert post('/api/auth/login/',{'username':username,'password':password}).status_code==200
            assert client.cookies['sessionid']['secure'] and client.cookies['sessionid']['httponly']
            assert client.get('/api/topic/a-temples/',secure=True).status_code==200
            assert post('/api/topic/a-temples/bookmark/',{'is_bookmarked':True}).status_code==200
            assert post('/api/topic/a-temples/progress/',{'is_completed':True}).status_code==200
            preview=client.get('/api/topic/a-temples/quiz/',secure=True).json()
            result=post('/api/topic/a-temples/quiz/submit/',{'quiz_id':preview['id'],'revision_token':preview['revision_token'],'answers':{},'submission_id':str(uuid.uuid4())})
            assert result.status_code==200
            assert post('/api/auth/register/',{}).status_code==503
            assert post('/api/auth/logout/',{}).status_code==200
            assert client.get('/api/topic/a-temples/',secure=True).status_code==401
            with transaction.atomic():
                from django.db import connection
                with connection.cursor() as cursor:cursor.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
                verify_install(public_demo=True);verify_runtime();verify_readiness()
        return {'controlled_runtime_login_csrf_read_owned_writes_logout':True,'controlled_runtime_post_use_readonly_verification':True}
    if kind=='fault':
        from unittest.mock import patch
        from django.core.management import call_command,CommandError
        with patch('content.services.sample_install.install_sample',side_effect=RuntimeError('synthetic injected failure')):
            try:call_command('initialize_free_demo',confirm_database=cfg['POSTGRES_DB'],staff_password_file=str(directory/'staff-password.txt'),apply=True,local_test=True)
            except CommandError:pass
            else:raise AssertionError('Failure injection did not run.')
        with connect(cfg,True,readonly=True) as c:assert objects(c)==[]
        return {'transactional_migration_and_seed_rollback':True}
    from django.test import Client
    client=Client(enforce_csrf_checks=True)
    basic='Basic '+base64.b64encode((cfg['STAGING_ACCESS_USERNAME']+':'+cfg['STAGING_ACCESS_PASSWORD']).encode()).decode()
    extra={'secure':True,'HTTP_AUTHORIZATION':basic}
    assert client.get('/api/config/',secure=True).status_code==401
    config_response=client.get('/api/config/',**extra);assert config_response.status_code==200
    assert config_response.json()['student_features_enabled'] is False
    assert client.get('/admin/login/',**extra).status_code==200
    token=client.cookies['csrftoken'].value
    password=(directory/'staff-password.txt').read_text().strip()
    response=client.post('/admin/login/',urlencode({'username':'sample-editor','password':password,'csrfmiddlewaretoken':token}),content_type='application/x-www-form-urlencoded',HTTP_ORIGIN='https://testserver',**extra)
    assert response.status_code==302
    assert client.get('/admin/content/topic/',**extra).status_code==200
    assert client.get('/api/topics/',**extra).status_code==200
    for path in ('/api/auth/register/','/api/dashboard/','/api/bookmarks/','/api/progress/','/api/plans/'):
        assert client.get(path,**extra).status_code==503
    assert client.post('/admin/content/topic/add/',{},**extra).status_code==403
    token=client.cookies['csrftoken'].value
    assert client.post('/admin/logout/',urlencode({'csrfmiddlewaretoken':token}),content_type='application/x-www-form-urlencoded',HTTP_ORIGIN='https://testserver',**extra).status_code in (200,302)
    assert '_auth_user_id' not in client.session
    return {'runtime_admin_login_read_logout_csrf':True,'runtime_public_api':True,'learner_and_editorial_gates':True}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--admin-config',type=Path,required=True)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--pg-bin',type=Path)
    p.add_argument('--expect-major',type=int,default=17)
    p.add_argument('--openssl',default='openssl')
    p.add_argument('--worker',choices=('http','fault','public-fault','public-http','public-refusals'))
    a=p.parse_args();os.umask(0o077)
    if a.worker:
        print(json.dumps(worker(a.worker,a.admin_config,a.directory)));return
    cfg=load_environment(a.admin_config)
    if cfg.get('POSTGRES_HOST')!='127.0.0.1' or not cfg.get('POSTGRES_DB','').startswith(('prepal_test_','prepal_free_demo_test_')):
        raise ValueError('Only explicit disposable loopback test credentials are accepted.')
    if a.directory.is_symlink():raise ValueError('Rehearsal directory cannot be a symlink.')
    root=a.directory.resolve();root.mkdir(mode=0o700,parents=True,exist_ok=False)
    with psycopg.connect(**connection_options(cfg)) as connection:
        assert connection.info.server_version//10000==a.expect_major, 'Unexpected PostgreSQL server major.'
    cfg.update(DATABASE_ENGINE='postgresql',PREPAL_FREE_DEMO='1',PREPAL_FREE_DEMO_SYNTHETIC_DATA='1')
    report={'local_only':True,'cases':{},'databases':[]}
    def new_target(label):
        name='prepal_free_demo_test_'+uuid.uuid4().hex[:12]
        # The operator base may be the CI prepal_test_* DB. Newly created targets
        # still pass the stricter prepal_free_demo_test_* guard in every workflow.
        with psycopg.connect(**connection_options(cfg),autocommit=True) as c:
            c.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
        env=cfg|{'POSTGRES_DB':name};path=root/(label+'.env')
        write_private(path,''.join(k+'='+json.dumps(v)+'\n' for k,v in env.items()))
        report['databases'].append(name)
        return env,path,root/(label+'-roles')
    def run(action,config,directory,name,apply=False,expect=0):
        args=[sys.executable,str(ROOT/'scripts/free_demo_database.py'),action,'--config',str(config),
              '--directory',str(directory),'--confirm-database',name,'--local-test']
        if apply:args.append('--apply')
        result=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
        with (root/'operations.log').open('a') as f:f.write(action+' '+str(result.returncode)+'\n'+result.stdout+result.stderr)
        if expect==0:assert result.returncode==0,action
        else:assert result.returncode!=0,action
        return json.loads(result.stdout) if result.returncode==0 else None
    env,path,directory=new_target('main');name=env['POSTGRES_DB']
    run('prepare',path,directory,name);run('roles',path,directory,name,True)
    migration=directory/'migration.env';runtime=directory/'runtime.env'
    result=run('initialize',migration,directory,name,True);assert result['changed'] is True
    result=run('initialize',migration,directory,name,True);assert result['changed'] is False
    report['counts']=result['counts'];report['cases']['initialize_and_idempotent_verify']=True
    run('grant-runtime',migration,directory,name,True);run('verify',runtime,directory,name)
    rcfg=load_environment(runtime)
    with connect(rcfg,True) as c:
        flags=c.execute('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls FROM pg_roles WHERE rolname=current_user').fetchone();assert not any(flags)
        for statement in ('CREATE TABLE should_not_exist(id integer)','CREATE TEMP TABLE should_not_exist(id integer)',
                          'ALTER TABLE content_topic ADD COLUMN should_not_exist integer',
                          "INSERT INTO content_topic(title,slug,\"order\",editorial_status) VALUES('rejected','rejected',0,'draft')",
                          'CREATE ROLE should_not_exist'):
            try:
                with c.transaction():c.execute(statement)
            except Exception as error:assert error.sqlstate=='42501'
            else:raise AssertionError('Runtime privilege escaped.')
    report['cases']['runtime_five_privilege_denials']=True
    value=subprocess.run([sys.executable,__file__,'--worker','http','--admin-config',str(runtime),'--directory',str(directory)],cwd=ROOT,capture_output=True,text=True)
    (root/'http.log').write_text(value.stdout+value.stderr);assert value.returncode==0
    report['cases'].update(json.loads(value.stdout))
    run('verify',runtime,directory,name)
    with connect(load_environment(migration),True) as c:
        c.execute('SELECT pg_advisory_xact_lock(738104,14215)')
        run('initialize',migration,directory,name,True,expect=1)
    report['cases']['concurrent_initializer_refused']=True
    # NEW second target proves migration DDL and data roll back as a unit.
    fault,fp,fd=new_target('fault');fn=fault['POSTGRES_DB']
    run('prepare',fp,fd,fn);run('roles',fp,fd,fn,True)
    value=subprocess.run([sys.executable,__file__,'--worker','fault','--admin-config',str(fd/'migration.env'),'--directory',str(fd)],cwd=ROOT,capture_output=True,text=True)
    (root/'fault.log').write_text(value.stdout+value.stderr);assert value.returncode==0
    report['cases'].update(json.loads(value.stdout))
    with connect(load_environment(fd/'migration.env'),True) as c:
        c.execute('CREATE TABLE unknown_data(id integer PRIMARY KEY,note text)');c.execute("INSERT INTO unknown_data VALUES(1,'synthetic unknown preserved')")
    run('initialize',fd/'migration.env',fd,fn,True,expect=1)
    with connect(load_environment(fd/'migration.env'),True,readonly=True) as c:assert c.execute('SELECT count(*) FROM unknown_data').fetchone()[0]==1
    report['cases']['unknown_data_preserved']=True
    if a.pg_bin:
        from content.services.postgres_backup import native_env,run as native_run,tool,extract
        mcfg=load_environment(migration)
        with connect(mcfg,True,readonly=True) as c:before=inventory(c)
        key=root/'recipient.key';cert=root/'recipient.pem'
        native_run([a.openssl,'req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(key),'-out',str(cert),'-subj','/CN=Prepal synthetic recovery','-days','1'])
        create_backup(migration,root/'encrypted-backup',cert,a.pg_bin,a.openssl,local=True)
        extract(root/'encrypted-backup/snapshot.cms',key,root/'decrypted',a.openssl)
        # A wrong recipient and authenticated-ciphertext tampering must never
        # yield an extraction directory or usable database dump.
        wrong_key=root/'wrong-recipient.key';wrong_cert=root/'wrong-recipient.pem'
        native_run([a.openssl,'req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(wrong_key),'-out',str(wrong_cert),'-subj','/CN=Wrong synthetic recipient','-days','1'])
        tampered=root/'tampered.cms'
        payload=bytearray((root/'encrypted-backup/snapshot.cms').read_bytes());payload[-1]^=1
        tampered.write_bytes(bytes(payload));tampered.chmod(0o600)
        for label,bundle,recipient in (('wrong-key',root/'encrypted-backup/snapshot.cms',wrong_key),('tampered',tampered,key)):
            destination=root/('rejected-'+label)
            try:extract(bundle,recipient,destination,a.openssl)
            except ValueError:assert not destination.exists()
            else:raise AssertionError('Unauthenticated backup was accepted.')
        assert key.stat().st_mode & 0o077==0 and root.stat().st_mode & 0o077==0
        report['cases']['recovery_wrong_key_and_tamper_refused']=True
        report['cases']['recovery_key_and_directory_private']=True
        plain=root/'decrypted/database.dump'
        restored,rp,rd=new_target('restored')
        # A fresh PostgreSQL database already has public. Omit only that schema's
        # CREATE entry; restore every table/index/constraint/sequence without DROP.
        listing=native_run([tool(a.pg_bin,'pg_restore'),'--list',str(plain)]).decode()
        entries=listing.splitlines()
        schema_entries=[line for line in entries if re.match(r'^\d+; \d+ \d+ SCHEMA - public(?: |$)',line)]
        assert len(schema_entries)==1
        toc=root/'restore-toc.list';toc.write_text('\n'.join(line for line in entries if line not in schema_entries)+'\n')
        native_run([tool(a.pg_bin,'pg_restore'),'--exit-on-error','--single-transaction','--no-owner','--no-acl','--use-list='+str(toc),'--dbname='+restored['POSTGRES_DB'],str(plain)],env=native_env(restored))
        with connect(restored,True,readonly=True) as c:report['restore']=verify_inventory(inventory(c),before)
        report['cases']['encrypted_native_independent_restore']=True
    # Additive transition on the already verified known synthetic corpus only.
    run('student-credentials',migration,directory,name)
    run('student-credentials',migration,directory,name,expect=1)  # Never overwrite a prepared credential.
    plan=run('student-login',migration,directory,name);assert plan['students']==0 and plan['changed'] is False
    for kind,config in (('public-fault',migration),):
        value=subprocess.run([sys.executable,__file__,'--worker',kind,'--admin-config',str(config),'--directory',str(directory)],cwd=ROOT,capture_output=True,text=True)
        (root/(kind+'.log')).write_text(value.stdout+value.stderr);assert value.returncode==0
        report['cases'].update(json.loads(value.stdout))
    added=run('student-login',migration,directory,name,True);assert added['changed'] and added['counts']['students']==1
    repeated=run('student-login',migration,directory,name,True);assert repeated['changed'] is False
    report['cases']['controlled_account_additive_and_repeat_safe']=True
    # The original empty-database initializer must refuse the extended state.
    run('initialize',migration,directory,name,True,expect=1)
    run('student-login',runtime,directory,name,True,expect=1)
    for kind,config in (('public-refusals',migration),('public-http',runtime)):
        value=subprocess.run([sys.executable,__file__,'--worker',kind,'--admin-config',str(config),'--directory',str(directory)],cwd=ROOT,capture_output=True,text=True)
        (root/(kind+'.log')).write_text(value.stdout+value.stderr);assert value.returncode==0
        report['cases'].update(json.loads(value.stdout))
    run('student-login',runtime,directory,name)
    report['public_demo_counts']=added['counts']
    with connect(env,True,readonly=True) as c:report['postgres_version']=c.info.server_version
    write_private(root/'result.json',json.dumps(report,indent=2));print(json.dumps(report,indent=2))


if __name__=='__main__':main()
