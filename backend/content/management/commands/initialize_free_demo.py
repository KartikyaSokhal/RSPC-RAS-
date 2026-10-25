"""Explicit PostgreSQL bootstrap. Never invoked by build/start or a request."""
import io
import json
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError, call_command
from django.db import connection, transaction
from django.db.migrations.loader import MigrationLoader
from content.services.free_demo_database import MARKER, target, corpus_digest
from content.services.postgres_ops import private_file


def relations():
    with connection.cursor() as c:
        c.execute("SELECT c.relname,c.relkind FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind IN ('r','p','v','m','S','f')")
        return dict(c.fetchall())


def verify_schema():
    expected={m._meta.db_table for m in apps.get_models(include_auto_created=True) if m._meta.managed and not m._meta.proxy}|{'django_migrations',MARKER}
    actual=relations()
    with connection.cursor() as c:
        c.execute("SELECT (SELECT count(*) FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname NOT IN ('public','information_schema'))+(SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname<>'information_schema')+(SELECT count(*) FROM pg_largeobject_metadata)+(SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='public' AND t.typtype IN ('d','e'))")
        if c.fetchone()[0]:raise ValueError('Unknown auxiliary schema/type/routine/large-object data preserved.')
    if {n for n,k in actual.items() if k!='S'}!=expected or any(k not in ('r','S') for k in actual.values()):
        raise ValueError('Unknown or incomplete database objects preserved.')
    with connection.cursor() as c:
        c.execute("SELECT c.relname FROM pg_class c WHERE c.oid IN (SELECT pg_get_serial_sequence(format('%I.%I',table_schema,table_name),column_name)::regclass FROM information_schema.columns WHERE table_schema='public' AND is_identity='YES')")
        if {n for n,k in actual.items() if k=='S'}!={r[0] for r in c.fetchall()}:
            raise ValueError('Unexpected standalone sequence preserved.')


def verify_install(*, public_demo=False):
    from content.services.sample_content import verify_sample
    verify_schema()
    loader=MigrationLoader(connection)
    if set(loader.applied_migrations)!=set(loader.disk_migrations) or len(loader.disk_migrations)!=30:
        raise ValueError('Migration state differs from reviewed30-migration graph.')
    with connection.cursor() as c:
        c.execute('SELECT metadata FROM '+MARKER+' WHERE id=1')
        row=c.fetchone()
        if not row: raise ValueError('Missing initialization identity marker.')
        meta=json.loads(row[0]) if isinstance(row[0],str) else row[0]
    expected_meta = {'version':1,'database':connection.settings_dict['NAME'],'corpus':corpus_digest()}
    student_meta = meta.get('public_demo') if isinstance(meta, dict) else None
    if public_demo:
        if (type(student_meta) is not dict or set(student_meta) != {'version', 'student_id', 'username'}
                or student_meta['version'] != 1 or type(student_meta['student_id']) is not int):
            raise ValueError('Controlled synthetic account marker is missing or invalid.')
        expected_meta['public_demo'] = student_meta
    if meta != expected_meta:
        raise ValueError('Marker or corpus identity mismatch; existing data preserved.')
    User=get_user_model()
    if User.objects.count() != (2 if public_demo else 1): raise ValueError('Unknown accounts preserved.')
    user=User.objects.get(username='sample-editor')
    if not user.is_staff or user.is_superuser or user.email or not user.is_active:
        raise ValueError('Synthetic staff identity mismatch.')
    if public_demo:
        from content.services.public_demo_database import verify_student
        verify_student(student_meta['student_id'], student_meta['username'])
    from django.contrib.auth.models import Permission,Group
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.management import _get_all_permissions
    models=list(apps.get_models())
    if set(ContentType.objects.values_list('app_label','model'))!={(m._meta.app_label,m._meta.model_name) for m in models}:
        raise ValueError('Unknown framework content types preserved.')
    expected_permissions={(m._meta.app_label,m._meta.model_name,code) for m in models for code,name in _get_all_permissions(m._meta)}
    if set(Permission.objects.values_list('content_type__app_label','content_type__model','codename'))!=expected_permissions:
        raise ValueError('Unknown framework permissions preserved.')
    if Group.objects.exists() or user.groups.exists() or set(user.user_permissions.values_list('pk',flat=True))!=set(Permission.objects.filter(codename__startswith='view_').values_list('pk',flat=True)):
        raise ValueError('Unexpected synthetic staff permissions preserved.')
    # Every non-corpus module must remain empty (framework metadata and sessions excluded).
    allowed={'Topic','ContentBlock','Quiz','Question','Choice','Tag','TopicAlias','TopicRelation',
             'KeywordLinkProposal','ConnectionScan','TopicPublication','QuizReview'}
    if public_demo:
        from content.services.public_demo_database import verify_owned_records
        verify_owned_records(student_meta['student_id'])
        allowed |= {'StudentIdentity','AuthRateWindow','Bookmark','UserProgress','QuizAttempt','StudyPlan','StudyTask'}
    for model in apps.get_app_config('content').get_models():
        if model.__name__ not in allowed and model.objects.exists():
            raise ValueError('Unexpected learner/media/provider data preserved.')
    report=verify_sample(learner_user_id=student_meta['student_id'] if public_demo else None)
    from content.models import KeywordLinkProposal,ConnectionScan
    if any(report[k]!=v for k,v in {'publications':30,'tags':19,'related_edges':30,'approved_links':30,'pending_links':0}.items()) or KeywordLinkProposal.objects.count()!=30 or ConnectionScan.objects.count()!=30:
        raise ValueError('Unknown connections or controlled registry rows preserved.')
    return report | {'migrations':30,'synthetic_staff':1,'students':int(public_demo),'uploads':0}


class Command(BaseCommand):
    help='Explicit guarded free-demo PostgreSQL initialization or read-only verification.'

    def add_arguments(self,p):
        p.add_argument('--confirm-database',required=True)
        p.add_argument('--staff-password-file')
        p.add_argument('--apply',action='store_true')
        p.add_argument('--local-test',action='store_true')

    def handle(self,*args,**opts):
        try:
            db=connection.settings_dict
            env={'DATABASE_ENGINE':'postgresql' if connection.vendor=='postgresql' else 'sqlite',
                 'POSTGRES_HOST':db['HOST'],'POSTGRES_DB':db['NAME'],
                 'POSTGRES_SSLMODE':db.get('OPTIONS',{}).get('sslmode'),
                 'PREPAL_FREE_DEMO':'1' if getattr(settings,'DEMO_MODE',False) else '0',
                 'PREPAL_FREE_DEMO_SYNTHETIC_DATA':__import__('os').environ.get('PREPAL_FREE_DEMO_SYNTHETIC_DATA')}
            target(env,opts['local_test'])
            if opts['confirm_database']!=db['NAME'] or settings.STUDENT_FEATURES_ENABLED or settings.AI_ENABLED:
                raise ValueError('Target confirmation or closed feature gates required.')
            if len(MigrationLoader(None).disk_migrations)!=30: raise ValueError('Reviewed migration graph changed.')
            if not opts['apply']:
                with transaction.atomic():
                    with connection.cursor() as c:
                        c.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
                        c.execute('SELECT current_database()=%s,current_user=%s',[db['NAME'],db['USER']])
                        if c.fetchone()!=(True,True):raise ValueError('Actual connection identity mismatch.')
                    report=verify_install()
                self.stdout.write(json.dumps({'verified':True,'changed':False,'counts':report}));return
            with connection.cursor() as c:
                c.execute('SELECT current_database()=%s,current_user=%s',[db['NAME'],db['USER']])
                if c.fetchone()!=(True,True):raise ValueError('Actual connection identity mismatch.')
                c.execute('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls FROM pg_roles WHERE rolname=current_user')
                if any(c.fetchone()):raise ValueError('Privileged administrative credentials cannot initialize the app.')
                c.execute("SELECT has_schema_privilege(current_user,'public','CREATE')")
                if not c.fetchone()[0]:raise ValueError('Explicit limited migration role required.')
            password=private_file(opts['staff_password_file']).read_text().strip()
            if len(password)<32: raise ValueError('Private strong synthetic staff password required.')
            with transaction.atomic():
                with connection.cursor() as c:
                    c.execute('SELECT pg_try_advisory_xact_lock(738104,14215)')
                    if not c.fetchone()[0]:raise ValueError('Another initializer owns the target lock.')
                if MARKER in relations():
                    if not get_user_model().objects.get(username='sample-editor').check_password(password):
                        raise ValueError('Existing staff password differs; no reset performed.')
                    report=verify_install();changed=False
                else:
                    with connection.cursor() as c:
                        if relations():raise ValueError('Existing/partial/unknown schema preserved; no reset is permitted.')
                        c.execute("SELECT count(*) FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname NOT IN ('public','information_schema')")
                        if c.fetchone()[0]:raise ValueError('Unknown schema preserved.')
                        c.execute("SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname<>'information_schema'")
                        if c.fetchone()[0]:raise ValueError('Unknown routines preserved.')
                        c.execute('SELECT count(*) FROM pg_largeobject_metadata')
                        if c.fetchone()[0]:raise ValueError('Existing large objects preserved.')
                        c.execute("SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='public' AND t.typtype IN ('d','e')")
                        if c.fetchone()[0]:raise ValueError('Unknown types preserved.')
                    # PostgreSQL transactional DDL: migrations, post_migrate permissions,
                    # corpus and completion marker commit together or all roll back.
                    call_command('migrate',interactive=False,verbosity=0,stdout=io.StringIO(),stderr=io.StringIO())
                    from content.services.sample_install import install_sample
                    install_sample(password,superuser=False)
                    from django.core.management.color import no_style
                    statements=connection.ops.sequence_reset_sql(no_style(),apps.get_app_config('content').get_models())
                    with connection.cursor() as c:
                        for statement in statements:c.execute(statement)
                        c.execute('CREATE TABLE '+MARKER+' (id integer PRIMARY KEY CHECK(id=1),metadata jsonb NOT NULL)')
                        c.execute('INSERT INTO '+MARKER+' VALUES (1,%s)',[json.dumps({'version':1,'database':db['NAME'],'corpus':corpus_digest()})])
                    report=verify_install();changed=True
            self.stdout.write(json.dumps({'verified':True,'changed':changed,'counts':report}))
        except Exception:
            # Never echo connection exceptions, SQL parameters, passwords or private rows.
            raise CommandError('Free-demo operation refused or failed; target preserved/transaction rolled back. Inspect identity, permissions, emptiness and reviewed corpus without printing secrets.') from None
