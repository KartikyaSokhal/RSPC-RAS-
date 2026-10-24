"""Rehearse SQLite -> PostgreSQL in new local databases only; never performs cutover.

Requires explicit POSTGRES_* environment variables (not backend/.env). Creates a
new prepal_rehearsal_* database and a NEW private directory. Refuses remote hosts.
No raw rows, credentials, prompts or SQL errors are printed. Freeze source/media
writes for a coherent backup. Private source data stays inside the local rehearsal.
"""
import argparse
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from content.services.backups import backup, restore, digest, inventory  # noqa: E402


def smoke_check():
    from django.contrib.auth import get_user_model
    from django.db import transaction
    from django.test import Client
    from content.models import Topic, ContentBlock, Quiz, Question, Choice, QuizAttempt
    from content.services.quiz import review_quiz
    checks = []
    guest = Client(enforce_csrf_checks=True)
    assert guest.get('/api/health/').status_code == 200
    assert guest.get('/api/topics/?tree=1').status_code == 200
    checks.append('health_and_public_syllabus')
    with transaction.atomic():
        password = secrets.token_urlsafe(24)
        editor = get_user_model().objects.create_superuser('phase1-rehearsal-editor-' + uuid.uuid4().hex[:8], password=password)
        client = Client(enforce_csrf_checks=True)
        assert client.get('/admin/login/').status_code == 200
        token = client.cookies['csrftoken'].value
        response = client.post('/admin/login/', {'username': editor.username, 'password': password, 'csrfmiddlewaretoken': token, 'next': '/admin/'})
        assert response.status_code == 302
        assert client.get('/admin/').status_code == 200
        checks.append('admin_session_login')
        blocked = ['/api/auth/register/', '/api/auth/login/', '/api/auth/logout/', '/api/auth/status/',
                   '/api/dashboard/', '/api/bookmarks/', '/api/progress/', '/api/profile/weaknesses/',
                   '/api/topic/not-a-topic/bookmark/', '/api/topic/not-a-topic/progress/', '/api/topic/not-a-topic/quiz/submit/']
        for identity in (guest, client):
            for url in blocked:
                response = identity.post(url, data='malformed', content_type='application/json')
                assert response.status_code == 503 and response.json()['error']['code'] == 'learner_features_unavailable'
        assert client.get(f'/admin/auth/user/{editor.pk}/report/').status_code == 403
        checks.append('guest_and_authenticated_learner_containment')
        topic = Topic.objects.create(title='Synthetic Phase 1 test', slug='phase1-' + uuid.uuid4().hex)
        ContentBlock.objects.create(topic=topic, block_type='text', content='<h2>Evidence</h2><p>A synthetic fact.</p><script>unsafe()</script>', order=1, source_reference='Synthetic rehearsal only')
        token = client.cookies['csrftoken'].value
        url = f'/admin/content/topic/{topic.pk}/change/'
        assert client.post(url, {'_publish_now': '1', 'csrfmiddlewaretoken': token}).status_code == 302
        detail = guest.get(f'/api/topic/{topic.slug}/').json()
        assert '<script' not in detail['blocks'][0]['content'] and '<h2>' in detail['blocks'][0]['content']
        checks.append('admin_publish_and_safe_public_reading')
        quiz = Quiz.objects.create(topic=topic, title='Synthetic reviewed practice')
        question = Question.objects.create(quiz=quiz, question_text='Which is supported?', explanation='Synthetic fact supports this.')
        choice = Choice.objects.create(question=question, choice_text='Synthetic fact', is_correct=True)
        Choice.objects.create(question=question, choice_text='Unsupported inference')
        assert guest.get(f'/api/topic/{topic.slug}/quiz/').status_code == 404
        review_quiz(quiz, editor, 'Synthetic rehearsal source')
        preview = guest.get(f'/api/topic/{topic.slug}/quiz/').json()
        guest.get('/api/config/')
        before = QuizAttempt.objects.count()
        for _ in range(2):
            result = guest.post(f'/api/topic/{topic.slug}/quiz/check/', {'quiz_id': quiz.pk, 'revision_token': preview['revision_token'], 'answers': {str(question.pk): choice.pk}}, content_type='application/json', HTTP_X_CSRFTOKEN=guest.cookies['csrftoken'].value)
            assert result.status_code == 200 and result.json()['score'] == 1
        assert QuizAttempt.objects.count() == before
        checks.append('reviewed_quiz_and_repeatable_stateless_grading')
        assert client.post(url, {'_withdraw_now': '1', 'csrfmiddlewaretoken': token}).status_code == 302
        assert guest.get(f'/api/topic/{topic.slug}/').json()['blocks'] == []
        checks.append('admin_withdrawal')
        transaction.set_rollback(True)
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sqlite-source', required=True)
    parser.add_argument('--source-media', required=True)
    parser.add_argument('--new-directory', required=True)
    args = parser.parse_args()
    os.umask(0o077)
    source = Path(args.sqlite_source).resolve(strict=True)
    original_hash = digest(source)
    root = Path(args.new_directory).resolve()
    root.mkdir(mode=0o700, parents=False, exist_ok=False)
    from core.database import database_config
    config = database_config({**os.environ, 'DATABASE_ENGINE': 'postgresql'})
    if config['HOST'] not in ('127.0.0.1', 'localhost', '::1'):
        raise ValueError('Rehearsal refuses remote PostgreSQL hosts.')
    backup_manifest = backup(source, args.source_media, root / 'backup')
    restored = restore(root / 'backup', root / 'restored')
    env = {**os.environ, 'PYTHON_DOTENV_DISABLED': '1', 'AI_ENABLED': 'false', 'AI_GUEST_ENABLED': 'false', 'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': ''}
    with (root / 'sqlite-migration.log').open('w') as log:
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/verify_migration.py'), str(root / 'restored/database.sqlite3'), str(root / 'migrated')], env=env, stdout=log, stderr=log)
    if result.returncode:
        raise ValueError('SQLite copy migration failed; see the private migration log.')
    migration_result = json.loads((root / 'sqlite-migration.log').read_text().splitlines()[-1])
    import psycopg
    from psycopg import sql
    name = 'prepal_rehearsal_' + uuid.uuid4().hex[:16]
    with psycopg.connect(dbname='postgres', user=config['USER'], password=config['PASSWORD'], host=config['HOST'], port=config['PORT'], **config['OPTIONS'], autocommit=True) as admin:
        admin.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
    os.environ.update(env)
    os.environ.update(DJANGO_SETTINGS_MODULE='core.rehearsal_settings', PREPAL_REHEARSAL='1', DATABASE_ENGINE='postgresql', POSTGRES_DB=name,
                      PREPAL_REHEARSAL_COPY=str(root / 'migrated/migration-copy.sqlite3'), DJANGO_ENV='development', DEBUG='false',
                      SECRET_KEY=secrets.token_urlsafe(48), PRIVATE_MEDIA_ROOT=str(root / 'restored/media'), STUDENT_FEATURES_ENABLED='false')
    import django
    django.setup()
    from django.core.management import call_command
    from django.db import connections
    from content.services.database_transfer import transfer, table_inventory, reset_and_verify_sequences
    with (root / 'postgres-migration.log').open('w') as log:
        call_command('migrate', interactive=False, verbosity=1, stdout=log, stderr=log)
    transfer_result = transfer()
    checks = smoke_check()
    assert table_inventory('source_copy') == table_inventory('default'), 'Smoke checks changed imported records.'
    transfer_result['sequences'] = reset_and_verify_sequences()
    assert digest(source) == original_hash and inventory(source) == backup_manifest['tables'], 'Original SQLite changed.'
    report = {'source_sha256': original_hash, 'source_unchanged': True, 'backup_restore': restored,
              'sqlite_migration': migration_result, 'postgres_database': name,
              'postgres_version': connections['default'].pg_version,
              'transfer': transfer_result, 'smoke_checks': checks, 'cutover': 'NOT_PERFORMED'}
    (root / 'result.json').write_text(json.dumps(report, indent=2))
    connections.close_all()
    print(json.dumps({k: v for k, v in report.items() if k != 'transfer'} | {'tables_compared': len(transfer_result['tables']), 'rows_transferred': transfer_result['rows'], 'sequences_verified': len(transfer_result['sequences'])}))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # SQL exception strings can contain private row values or connection details.
        import traceback
        traceback.print_tb(exc.__traceback__)
        print(json.dumps({'status': 'FAILED', 'error_type': type(exc).__name__, 'cutover': 'NOT_PERFORMED', 'detail': 'Inspect the private rehearsal logs; no SQL/record/credential values emitted.'}), file=sys.stderr)
        sys.exit(1)
