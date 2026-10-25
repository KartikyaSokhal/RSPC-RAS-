"""Additive controlled synthetic-account transition; no reset or startup writes."""
import json
import re
from django.contrib.auth import get_user_model
from django.db import connection, transaction
from psycopg import sql
from .free_demo_database import MARKER

OWNED_TABLES = ('django_session', 'content_authratewindow', 'content_bookmark', 'content_userprogress',
                'content_quizattempt', 'content_quizattempt_incorrect_questions',
                'content_studyplan', 'content_studyplan_selected_topics', 'content_studytask')
LOCK_TABLES = ('content_question', 'content_choice', 'content_quiz', 'content_quizreview', 'content_topicpublication')


def verify_student(pk, username):
    from content.models import StudentIdentity
    user = get_user_model().objects.get(pk=pk)
    if (not re.fullmatch(r'prepal-demo-[a-f0-9]{24}', username) or user.username != username or user.email != username+'@example.invalid' or user.first_name != 'Synthetic demo'
            or user.last_name or not user.is_active or user.is_staff or user.is_superuser
            or not user.has_usable_password() or user.groups.exists() or user.user_permissions.exists()
            or StudentIdentity.objects.count() != 1
            or not StudentIdentity.objects.filter(user=user, email=user.email, google_subject__isnull=True).exists()):
        raise ValueError('Unknown or altered synthetic identity preserved.')
    return user


def verify_owned_records(pk):
    from content.models import Bookmark, UserProgress, QuizAttempt, StudyPlan, StudyTask
    for model in (Bookmark, UserProgress, QuizAttempt, StudyPlan):
        if model.objects.exclude(user_id=pk).exists():
            raise ValueError('Unknown or ownerless learner records preserved.')
    if StudyTask.objects.exclude(plan__user_id=pk).exists():
        raise ValueError('Unknown study tasks preserved.')


def verify_runtime(role=None):
    role = role or connection.settings_dict['USER']
    with connection.cursor() as c:
        c.execute("""SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls,
            has_schema_privilege(rolname,'public','CREATE'),
            has_database_privilege(rolname,current_database(),'CREATE'),
            has_database_privilege(rolname,current_database(),'TEMP'),
            EXISTS(SELECT 1 FROM pg_auth_members WHERE member=r.oid),
            EXISTS(SELECT 1 FROM pg_class WHERE relnamespace='public'::regnamespace AND relowner=r.oid)
            FROM pg_roles r WHERE rolname=%s""", [role])
        if c.fetchone() != (False,)*10: raise ValueError('Unsafe runtime flags, ownership, membership or DDL privileges.')
        c.execute("""SELECT bool_and(has_table_privilege(%s,t,p)) FROM unnest(%s::text[]) t
            CROSS JOIN unnest(ARRAY['SELECT','INSERT','UPDATE','DELETE']) p""", [role,list(OWNED_TABLES)])
        if c.fetchone()[0] is not True: raise ValueError('Missing owned-record runtime grants.')
        c.execute("""SELECT bool_and(has_column_privilege(%s,t,'id','UPDATE')
            AND NOT has_table_privilege(%s,t,'UPDATE') AND NOT has_table_privilege(%s,t,'INSERT')
            AND NOT has_table_privilege(%s,t,'DELETE')) FROM unnest(%s::text[]) t""", [role]*4+[list(LOCK_TABLES)])
        if c.fetchone()[0] is not True: raise ValueError('Missing row-lock or overbroad canonical-content grants.')
        c.execute("""SELECT bool_and(has_sequence_privilege(%s,pg_get_serial_sequence(t,'id'),'USAGE'))
            FROM unnest(%s::text[]) t""", [role,[t for t in OWNED_TABLES if t!='django_session']])
        if c.fetchone()[0] is not True: raise ValueError('Missing owned-record sequence usage.')


def verify_readiness():
    """Bounded startup check; exhaustive corpus revalidation belongs to operator preflight."""
    from django.apps import apps
    from django.db.migrations.loader import MigrationLoader
    from content.management.commands.initialize_free_demo import verify_schema
    from .free_demo_database import corpus_digest
    expected = {'Topic':142,'ContentBlock':15,'Quiz':15,'Question':75,'Choice':300,
                'QuizReview':15,'Tag':19,'TopicAlias':15,'TopicRelation':30,
                'KeywordLinkProposal':30,'ConnectionScan':30,'TopicPublication':30}
    owned = {'StudentIdentity','AuthRateWindow','Bookmark','UserProgress','QuizAttempt','StudyPlan','StudyTask'}
    verify_schema()
    with connection.cursor() as c:
        c.execute('SELECT metadata FROM '+MARKER+' WHERE id=1')
        raw = c.fetchone()[0]
        meta = json.loads(raw) if isinstance(raw,str) else raw
        student = meta.get('public_demo',{})
        if (set(student) != {'version','student_id','username'} or student['version'] != 1
                or type(student['student_id']) is not int
                or meta != {'version':1,'database':connection.settings_dict['NAME'],
                            'corpus':corpus_digest(),'public_demo':student}):
            raise ValueError('Wrong corpus/database/controlled-account marker.')
        c.execute('SELECT app,name FROM django_migrations')
        if set(c.fetchall()) != set(MigrationLoader(None).disk_migrations):
            raise ValueError('Unexpected migration state.')
        models=list(apps.get_app_config('content').get_models())
        query=sql.SQL(' UNION ALL ').join(sql.SQL('SELECT {},count(*) FROM {}').format(sql.Literal(m.__name__),sql.Identifier(m._meta.db_table)) for m in models)
        c.execute(query);counts=dict(c.fetchall())
    for name,count in counts.items():
        if name not in owned and count != expected.get(name,0): raise ValueError('Unexpected corpus/media/provider counts.')
    User=get_user_model()
    if User.objects.count()!=2: raise ValueError('Unknown accounts preserved.')
    staff=User.objects.get(username='sample-editor')
    if not staff.is_staff or staff.is_superuser or not staff.is_active or staff.email:
        raise ValueError('Unexpected staff identity.')
    verify_student(student['student_id'], student['username']);verify_owned_records(student['student_id']);verify_runtime()
    return {'topics':142,'lessons':15,'quizzes':15,'questions':75,'choices':300,'students':1,'synthetic_staff':1,'uploads':0,'migrations':30}


def transition(username, password, *, apply=False, runtime_role=None):
    from content.management.commands.initialize_free_demo import verify_install
    from content.models import StudentIdentity
    if connection.vendor != 'postgresql' or not re.fullmatch(r'prepal-demo-[a-f0-9]{24}', username) or len(password) < 32:
        raise ValueError('Explicit PostgreSQL and private strong synthetic password required.')
    with transaction.atomic():
        with connection.cursor() as c:
            if not apply: c.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
            if apply:
                c.execute('SELECT pg_try_advisory_xact_lock(738104,14215)')
                if not c.fetchone()[0]: raise ValueError('Another demo operator is active.')
                c.execute("SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls,has_schema_privilege(current_user,'public','CREATE') FROM pg_roles WHERE rolname=current_user")
                flags = c.fetchone()
                if any(flags[:5]) or not flags[5]: raise ValueError('Restricted migration owner required.')
            c.execute('SELECT metadata FROM '+MARKER+' WHERE id=1')
            raw = c.fetchone()[0]
        meta = json.loads(raw) if isinstance(raw, str) else raw
        changed = False
        if 'public_demo' not in meta:
            verify_install()  # Exact original corpus, one staff, no learner/AI/media data.
            if not apply: return {'ready_to_prepare': True, 'changed': False, 'students': 0}
            user = get_user_model().objects.create_user(username, email=username+'@example.invalid', password=password, first_name='Synthetic demo')
            StudentIdentity.objects.create(user=user, email=user.email)
            meta['public_demo'] = {'version': 1, 'student_id': user.pk, 'username': username}
            with connection.cursor() as c:
                c.execute('UPDATE '+MARKER+' SET metadata=%s WHERE id=1', [json.dumps(meta)])
            changed = True
        else:
            user = verify_student(meta['public_demo']['student_id'], username)
            if not user.check_password(password): raise ValueError('Password mismatch; never reset existing credentials.')
        counts = verify_install(public_demo=True)
        if apply and runtime_role:
            # Fixed table list and quoted role; no arbitrary privilege/SQL input.
            with connection.cursor() as c:
                c.execute('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls FROM pg_roles WHERE rolname=%s', [runtime_role])
                if c.fetchone() != (False,)*5: raise ValueError('Unsafe runtime role.')
                for table in OWNED_TABLES:
                    c.execute(sql.SQL('GRANT SELECT,INSERT,UPDATE,DELETE ON {} TO {}').format(sql.Identifier(table),sql.Identifier(runtime_role)))
                    sequence = None
                    if table != 'django_session':
                        c.execute('SELECT pg_get_serial_sequence(%s,\'id\')', [table])
                        sequence = c.fetchone()[0]
                    if sequence: c.execute(sql.SQL('GRANT USAGE ON SEQUENCE {} TO {}').format(sql.Identifier(*sequence.split('.')),sql.Identifier(runtime_role)))
                for table in LOCK_TABLES:
                    c.execute(sql.SQL('GRANT UPDATE(id) ON {} TO {}').format(sql.Identifier(table),sql.Identifier(runtime_role)))
            verify_runtime(runtime_role)
        elif runtime_role:
            verify_runtime(runtime_role)
        return {'changed': changed, 'verified': True, 'counts': counts, 'runtime_grants_verified': bool(runtime_role)}


def read_public_marker():
    with connection.cursor() as cursor:
        cursor.execute('SELECT metadata FROM '+MARKER+' WHERE id=1')
        raw=cursor.fetchone()[0]
    return (json.loads(raw) if isinstance(raw,str) else raw)['public_demo']


def matches_controlled_student(user):
    from django.db import DatabaseError
    try:
        marker=read_public_marker()
        username=marker['username']
        return (set(marker)=={'version','student_id','username'} and marker['version']==1 and type(marker['student_id']) is int and user.pk==marker['student_id']
                and re.fullmatch(r'prepal-demo-[a-f0-9]{24}',username) is not None
                and user.username==username and user.email==username+'@example.invalid'
                and user.student_identity.email==user.email)
    except (DatabaseError,ValueError,KeyError,TypeError,IndexError):
        return False
