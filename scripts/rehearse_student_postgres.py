"""NEW local PG rehearsal from a verified SQLite backup. Never switches running app.

Requires explicit admin credentials, copied source and new destination; all
synthetic writes, native encrypted backups and restores stay disposable/local.
"""
import argparse
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
import uuid
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from content.services.postgres_ops import load_environment, provision_local, write_private, connection_options
from content.services.postgres_backup import backup, extract, restore_local, run
from content.services.backups import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('admin-env', 'sqlite-copy', 'media-copy', 'new-directory', 'pg-bin'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--openssl', default='openssl')
    args = parser.parse_args(); os.umask(0o077)
    root = Path(args.new_directory).resolve(); root.mkdir(mode=0o700, exist_ok=False)
    source = Path(args.sqlite_copy).resolve(strict=True); source_hash = digest(source)
    admin = load_environment(args.admin_env)
    name = 'prepal_rehearsal_student_' + uuid.uuid4().hex[:10]
    provision = provision_local(admin, name, root / 'credentials')
    env = load_environment(root / 'credentials/migration.env')
    common = {'PYTHON_DOTENV_DISABLED': '1', 'DJANGO_ENV': 'development', 'DEBUG': 'false',
              'ALLOWED_HOSTS': '127.0.0.1,localhost,testserver', 'PRIVATE_MEDIA_ROOT': str(root / 'media'),
              'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend'}
    with (root / 'copy-migration.log').open('w') as log:
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/verify_migration.py'), str(source), str(root / 'migrated')], env=os.environ | env | common, stdout=log, stderr=log)
        if result.returncode: raise ValueError('Copied SQLite migration failed.')
    media = root / 'media'; media.mkdir(mode=0o700)
    import shutil
    if Path(args.media_copy).is_dir(): shutil.copytree(args.media_copy, media, dirs_exist_ok=True)
    os.environ.update(env | common | {'DJANGO_SETTINGS_MODULE': 'core.rehearsal_settings', 'PREPAL_REHEARSAL': '1',
                                    'PREPAL_REHEARSAL_COPY': str(root / 'migrated/migration-copy.sqlite3')})
    import django
    django.setup()
    from django.conf import settings
    from django.core.management import call_command
    from django.db import connections
    from content.services.database_transfer import transfer
    with (root / 'pg-migration.log').open('w') as log: call_command('migrate', interactive=False, stdout=log, stderr=log)
    transferred = transfer()
    postgres_version = connections['default'].pg_version
    write_private(root / 'transfer.json', json.dumps(transferred, indent=2))
    # Application behavior now runs with the limited runtime role, not migration credentials.
    runtime = load_environment(root / 'credentials/runtime.env') | common | {'STUDENT_FEATURES_ENABLED': 'true', 'DJANGO_SETTINGS_MODULE': 'core.local_postgres_settings'}
    write_private(root / 'candidate-runtime.env', ''.join(f'{k}={json.dumps(str(v))}\n' for k,v in sorted(runtime.items())))
    connections.close_all()
    connections['default'].settings_dict.update(USER=runtime['POSTGRES_USER'], PASSWORD=runtime['POSTGRES_PASSWORD'])
    settings.STUDENT_FEATURES_ENABLED = True
    settings.EMAIL_BACKEND = common['EMAIL_BACKEND']
    from django.contrib.auth import get_user_model
    from content.models import Topic, ContentBlock, Bookmark, UserProgress, Quiz, Question, Choice, QuizAttempt, StudyPlan, StudyTask
    from content.services.publication import publish
    from content.services.quiz import review_quiz
    from rest_framework.test import APIClient
    editor = get_user_model().objects.filter(is_superuser=True).first()
    assert editor is not None
    subject = Topic.objects.create(title='Recovery drill subject', slug='recovery-subject')
    publish(subject, editor)
    topic = Topic.objects.create(title='Recovery drill lesson', slug='recovery-lesson', parent=subject)
    ContentBlock.objects.create(topic=topic, block_type='text', content='<h2>Recovery fixture</h2><p>Synthetic recovery evidence.</p>', source_reference='Synthetic recovery drill only', order=1)
    publish(topic, editor)
    quiz = Quiz.objects.create(topic=topic, title='Recovery reviewed quiz')
    question = Question.objects.create(quiz=quiz, primary_topic=topic, question_text='What is verified?', explanation='Recovery is verified in this fixture.')
    correct = Choice.objects.create(question=question, choice_text='Recovery', is_correct=True)
    Choice.objects.create(question=question, choice_text='An unsupported claim')
    review_quiz(quiz, editor, 'Synthetic native recovery drill')
    first = APIClient(enforce_csrf_checks=True); other = APIClient(enforce_csrf_checks=True)
    password = secrets.token_urlsafe(30)
    def post(client, route, data):
        token = client.get('/api/config/').json()['csrf_token']
        return client.post('/api/' + route, data, format='json', HTTP_X_CSRFTOKEN=token)
    for client, username in [(first, 'recovery_first'), (other, 'recovery_other')]:
        assert post(client, 'auth/register/', {'username': username, 'email': username + '@example.invalid', 'password': password}).status_code == 200
    user = get_user_model().objects.get(username='recovery_first')
    assert user.check_password(password) and user.password != password
    for _ in range(2):
        assert post(first, 'topic/recovery-lesson/bookmark/', {'is_bookmarked': True}).status_code == 200
        assert post(first, 'topic/recovery-lesson/progress/', {'is_completed': True}).status_code == 200
    assert post(first, 'topic/recovery-lesson/visit/', {}).status_code == 200
    assert Bookmark.objects.filter(user=user).count() == UserProgress.objects.filter(user=user).count() == 1
    preview = first.get('/api/topic/recovery-lesson/quiz/').json()
    payload = {'quiz_id': quiz.pk, 'revision_token': preview['revision_token'], 'answers': {str(question.pk): correct.pk}, 'submission_id': str(uuid.uuid4())}
    saved = post(first, 'topic/recovery-lesson/quiz/submit/', payload)
    assert saved.status_code == 200
    assert post(first, 'topic/recovery-lesson/quiz/submit/', payload).json() == saved.json()
    attempt_id = saved.json()['attempt_id']; assert QuizAttempt.objects.filter(user=user).count() == 1
    immutable = first.get(f'/api/attempts/{attempt_id}/').json()
    question.question_text = 'Changed after assessment'; question.save()
    assert first.get(f'/api/attempts/{attempt_id}/').json() == immutable
    plan = post(first, 'plans/', {'title': 'Recovery drill plan', 'mode': 'learn', 'study_days': [0,2,4], 'daily_minutes': 60,
                                'default_estimate_minutes': 90, 'start_date': '2026-10-26', 'exam_date': None, 'topic_ids': [subject.pk]}).json()
    task = plan['tasks'][0]
    completed = post(first, f'plans/{plan["id"]}/tasks/{task["id"]}/', {'is_completed': True}).json()
    task_before = StudyTask.objects.get(pk=task['id']); historical = (task_before.completed_at, task_before.minutes)
    assert post(first, f'plans/{plan["id"]}/reschedule/', {'revision': completed['revision'], 'start_date': '2026-11-02'}).status_code == 200
    task_before.refresh_from_db(); assert historical == (task_before.completed_at, task_before.minutes)
    assert other.get(f'/api/plans/{plan["id"]}/').status_code == 404
    assert other.get(f'/api/attempts/{attempt_id}/').status_code == 404
    assert other.get('/api/dashboard/').json()['stats']['total_bookmarks'] == 0
    assert other.get('/api/dashboard/').json()['stats']['total_completed'] == 0
    assert post(first, 'account/deletion/', {'password': password, 'confirmation': 'DELETE MY ACCOUNT'}).status_code == 409
    assert get_user_model().objects.filter(pk=user.pk).exists()
    # The same persisted DB session must survive actual backend process termination/restart.
    cookie = first.cookies[settings.SESSION_COOKIE_NAME].value
    http_checks = []
    for iteration in range(2):
        with (root / f'backend-{iteration}.log').open('w') as log:
            process = subprocess.Popen([sys.executable, str(ROOT / 'backend/manage.py'), 'runserver', '127.0.0.1:8003', '--noreload'], env=os.environ | runtime, stdout=log, stderr=log)
            try:
                for wait in range(100):
                    try:
                        request = Request('http://127.0.0.1:8003/api/dashboard/', headers={'Cookie': settings.SESSION_COOKIE_NAME + '=' + cookie})
                        with urlopen(request, timeout=1) as response: data = json.load(response)
                        assert data['stats']['total_bookmarks'] == 1 and data['stats']['total_completed'] == 1 and data['stats']['total_quizzes_taken'] == 1
                        http_checks.append('persisted_session_and_owned_dashboard_after_start_' + str(iteration)); break
                    except OSError:
                        if process.poll() is not None: raise ValueError('Candidate backend did not start.')
                        time.sleep(.1)
                else: raise ValueError('Candidate backend readiness timeout.')
            finally:
                process.terminate(); process.wait(timeout=10)
    connections.close_all()
    # Runtime DDL and backup DML must be denied; no protected data is used here.
    import psycopg
    denied = []
    for role, sqls in [('runtime', ['CREATE TABLE public.should_not_exist (id integer)', 'ALTER TABLE content_topic ADD COLUMN should_not_exist integer', "SELECT setval('content_topic_id_seq',999999)"]),
                       ('backup', ['DELETE FROM content_topic', 'CREATE TABLE public.should_not_exist (id integer)'])]:
        credentials = load_environment(root / f'credentials/{role}.env')
        for statement in sqls:
            with psycopg.connect(**connection_options(credentials)) as connection:
                try: connection.execute(statement)
                except psycopg.errors.InsufficientPrivilege: denied.append(role + '_denied')
                else: raise ValueError('Least privilege check failed.')
    # Exercise pairing with a synthetic private media file, without changing source media.
    write_private(media / 'synthetic-recovery.txt', 'Synthetic recovery verification only.\n')
    run([args.openssl, 'req', '-x509', '-newkey', 'rsa:3072', '-nodes', '-days', '2', '-subj', '/CN=Prepal local recovery drill',
         '-keyout', str(root / 'recipient-private.pem'), '-out', str(root / 'recipient.crt')])
    os.chmod(root / 'recipient-private.pem', 0o600)
    backup_env = load_environment(root / 'credentials/backup.env')
    assert 'SECRET_KEY' not in backup_env
    receipt = backup(backup_env, media, root / 'encrypted-backups', root / 'recipient.crt', args.pg_bin, args.openssl)
    bundle = root / 'encrypted-backups' / receipt['file']
    result = restore_local(admin, 'prepal_rehearsal_restore_' + uuid.uuid4().hex[:10], bundle, root / 'recipient-private.pem', root / 'independent-restore', args.pg_bin, args.openssl)
    # Reuse original Django signing key on restored DB to prove session/hash/snapshot portability.
    restored_env = load_environment(root / 'independent-restore/credentials/runtime.env')
    connections['default'].settings_dict.update(NAME=restored_env['POSTGRES_DB'], USER=restored_env['POSTGRES_USER'], PASSWORD=restored_env['POSTGRES_PASSWORD'])
    assert first.get('/api/auth/status/').json()['authenticated']
    assert first.get(f'/api/attempts/{attempt_id}/').json() == immutable
    restored_task = StudyTask.objects.get(pk=task['id']); assert (restored_task.completed_at, restored_task.minutes) == historical
    assert get_user_model().objects.get(pk=user.pk).check_password(password)
    assert other.get(f'/api/plans/{plan["id"]}/').status_code == 404
    assert first.get('/api/dashboard/').json()['stats']['total_completed'] == 1
    connections.close_all()
    negative = []
    for kind in ('tampered', 'truncated'):
        data = bytearray(bundle.read_bytes())
        if kind == 'tampered': data[len(data)//2] ^= 1
        else: data = data[:len(data)//2]
        damaged = root / (kind + '.cms'); damaged.write_bytes(data); damaged.chmod(0o600)
        try: extract(damaged, root / 'recipient-private.pem', root / ('reject-' + kind), args.openssl)
        except ValueError: negative.append(kind)
        else: raise ValueError('Damaged encrypted backup accepted.')
    run([args.openssl, 'req', '-x509', '-newkey', 'rsa:2048', '-noenc', '-days', '1', '-subj', '/CN=Wrong drill recipient',
         '-keyout', str(root / 'wrong-private.pem'), '-out', str(root / 'wrong.crt')])
    os.chmod(root / 'wrong-private.pem', 0o600)
    try: extract(bundle, root / 'wrong-private.pem', root / 'reject-wrong-key', args.openssl)
    except ValueError: negative.append('wrong_private_key')
    else: raise ValueError('Wrong recovery key accepted.')
    assert digest(source) == source_hash
    report = {'cutover': 'NOT_PERFORMED', 'source_copy_unchanged': True, 'postgres_version': postgres_version,
              'source_tables': len(transferred['tables']), 'source_rows': transferred['rows'], 'source_sequences': len(transferred['sequences']),
              'foreign_keys': transferred['foreign_keys_verified'], 'http_restart_checks': http_checks, 'privilege_rejections': len(denied),
              'independent_restore': result, 'encrypted_media_verified': 1, 'corrupt_backup_rejections': negative,
              'student_checks': ['hashed_passwords', 'sessions', 'owned_bookmark_idempotence', 'completion_idempotence', 'visits',
                                 'immutable_attempts', 'planner_history', 'cross_user_isolation', 'deletion_policy_gate', 'restored_session_and_learning_data'],
              'candidate_database': name, 'production_tls': 'configuration_only_local_runtime_has_no_SSL', 'synthetic_only': True}
    write_private(root / 'result.json', json.dumps(report, indent=2)); print(json.dumps(report))


if __name__ == '__main__':
    try: main()
    except Exception as error:
        # No exception string/traceback: SQL, credentials and learner rows can be sensitive.
        print(json.dumps({'status': 'FAILED', 'error_type': type(error).__name__, 'cutover': 'NOT_PERFORMED'}), file=sys.stderr); sys.exit(1)
