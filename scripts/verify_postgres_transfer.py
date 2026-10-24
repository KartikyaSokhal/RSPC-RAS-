"""Synthetic PostgreSQL transfer regression, including framework/M2M IDs and deleted-ID counters.

Uses real migrations in a new temporary SQLite fixture, then the same isolated
rehearsal process as real-data copies. Reads explicit POSTGRES_* env; no .env load.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def seed_worker(directory):
    directory = Path(directory).resolve()
    expected = directory / 'synthetic-source.sqlite3'
    if not directory.name.startswith('prepal-transfer-fixture-') or Path(os.environ.get('DATABASE_PATH', '')).resolve() != expected:
        raise ValueError('Refusing synthetic records outside a fresh fixture directory.')
    sys.path.insert(0, str(ROOT / 'backend'))
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group, Permission
    from django.contrib.admin.models import LogEntry, ADDITION
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.sessions.models import Session
    from django.core.files.base import ContentFile
    from django.utils import timezone
    from content.models import Topic, ContentBlock, Quiz, Question, Choice, Bookmark, UserProgress, QuizAttempt, TopicRelation, LearningResource, ResourcePage, AiBudgetBucket, AiRequest, Tag, TopicAlias
    from content.services.publication import publish
    from content.services.quiz import review_quiz
    from content.management.commands.create_demo import demo_pdf
    import hashlib
    import uuid
    User = get_user_model()
    editor = User.objects.create_superuser('synthetic-editor', password='fixture-only-unused')
    learner = User.objects.create_user('synthetic-legacy-learner', password='fixture-only-unused')
    from content.models import StudentIdentity, AuthRateWindow, StudyPlan, StudyTask
    StudentIdentity.objects.create(user=learner, email='synthetic-transfer@example.test')
    AuthRateWindow.objects.create(key='synthetic-transfer-window', count=2)
    group = Group.objects.create(name='Synthetic editorial group')
    permission = Permission.objects.filter(content_type__app_label='content', codename='change_topic').get()
    User.groups.through.objects.create(pk=401, user=editor, group=group)
    User.user_permissions.through.objects.create(pk=402, user=editor, permission=permission)
    Group.permissions.through.objects.create(pk=403, group=group, permission=permission)
    topic = Topic.objects.create(title='Synthetic root', slug='synthetic-transfer-root')
    child = Topic.objects.create(title='Synthetic child', slug='synthetic-transfer-child', parent=topic)
    TopicRelation.objects.create(source=topic, target=child, kind='related', status='approved', reason='Synthetic fixture relationship')
    block = ContentBlock.objects.create(topic=topic, block_type='text', content='<h2>Evidence</h2><p>Unicode: राजस्थान</p>', source_reference='Synthetic fixture', order=1)
    tag = Tag.objects.create(name='Controlled राजस्थान', is_public=True)
    topic.tags.add(tag)
    TopicAlias.objects.create(topic=child, name='Synthetic alias', status='approved')
    block.content += '<p>A Synthetic alias explains published evidence.</p>'
    block.save()
    ContentBlock.objects.create(topic=child, block_type='text', content='<p>Reviewed synthetic child explanation.</p>', source_reference='Synthetic', order=1)
    publish(topic, editor)
    publish(child, editor)
    payload = demo_pdf('Synthetic transfer fixture')
    resource = LearningResource(topic=topic, title='Synthetic PDF', status='approved', source_reference='Synthetic fixture only', rights_note='Original generated fixture', sha256=hashlib.sha256(payload).hexdigest(), byte_count=len(payload), page_count=1, reviewed_by=editor, reviewed_at=timezone.now())
    resource.file.save('fixture.pdf', ContentFile(payload), save=True)
    ResourcePage.objects.create(resource=resource, page_number=1, text='Synthetic extracted page.', text_sha256=hashlib.sha256(b'Synthetic extracted page.').hexdigest())
    block.content += '<p>Revised fixture.</p>'
    block.save()
    publish(topic, editor)
    quiz = Quiz.objects.create(topic=topic, title='Synthetic reviewed quiz')
    question = Question.objects.create(quiz=quiz, question_text='Which is supported?', explanation='Synthetic explanation.')
    Choice.objects.create(question=question, choice_text='Evidence', is_correct=True)
    Choice.objects.create(question=question, choice_text='Unsupported claim')
    question.related_topics.add(child)
    question.tags.add(tag)
    review_quiz(quiz, editor, 'Synthetic review only')
    from content.models import KeywordLinkProposal, TopicPublication
    from content.services.connections import decide
    revision = TopicPublication.objects.get(topic=topic).revision
    proposal = KeywordLinkProposal.objects.get(source=topic, target=child, source_revision=revision, phrase_key='synthetic alias')
    decide(proposal, 'approved', editor)
    for owner in (None, learner):
        Bookmark.objects.create(topic=topic, user=owner)
        UserProgress.objects.create(topic=topic, user=owner, is_completed=True, last_visited_at=timezone.now() if owner else None)
        attempt = QuizAttempt.objects.create(quiz=quiz, user=owner, score=0, total_questions=1,
            submission_id=uuid.uuid4() if owner else None,
            snapshot={'version': 1, 'title': 'Synthetic historical practice', 'results': [{'question_id': question.pk, 'question_text': question.question_text}]} if owner else {})
        attempt.incorrect_questions.add(question)
    plan = StudyPlan.objects.create(user=learner, title='Synthetic transfer plan', mode='learn', study_days=[0, 2], daily_minutes=60,
                                   default_estimate_minutes=90, start_date=timezone.localdate())
    plan.selected_topics.add(topic)
    StudyTask.objects.create(plan=plan, topic=topic, topic_title=topic.title, kind='learn', due_date=plan.start_date,
                             minutes=30, sequence=0, is_completed=True, completed_at=timezone.now())
    through = QuizAttempt.incorrect_questions.through.objects.first()
    old = through.pk
    QuizAttempt.incorrect_questions.through.objects.filter(pk=old).update(id=777)
    Session.objects.create(session_key='synthetic-transfer-session', session_data='synthetic-opaque-data', expire_date=timezone.now())
    LogEntry.objects.create(user=editor, content_type=ContentType.objects.get_for_model(Topic), object_id=str(topic.pk), object_repr='Synthetic fixture log', action_flag=ADDITION, change_message='Synthetic')
    AiBudgetBucket.objects.create(key='synthetic-bucket', reserved_micro=12345, requests=2)
    AiRequest.objects.create(request_id=uuid.uuid4(), visitor_key='synthetic', bucket_keys=['synthetic-bucket'], reserved_micro=12345, actual_micro=10000, state='completed', model='mock-only', deadline_at=timezone.now())
    deleted = Topic.objects.create(pk=9000, title='Deleted fixture', slug='deleted-fixture')
    deleted.delete()
    deleted_link = User.groups.through.objects.create(pk=9001, user=learner, group=group)
    deleted_link.delete()


def main():
    os.umask(0o077)
    directory = Path(tempfile.mkdtemp(prefix='prepal-transfer-fixture-'))
    env = {**os.environ, 'DJANGO_SETTINGS_MODULE': 'core.settings', 'DATABASE_ENGINE': 'sqlite',
           'DATABASE_PATH': str(directory / 'synthetic-source.sqlite3'), 'PRIVATE_MEDIA_ROOT': str(directory / 'media'),
           'PYTHON_DOTENV_DISABLED': '1', 'DJANGO_ENV': 'development', 'AI_ENABLED': 'false', 'AI_GUEST_ENABLED': 'false', 'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': ''}
    commands = [([sys.executable, str(ROOT / 'backend/manage.py'), 'migrate', '--noinput'], env),
                ([sys.executable, str(Path(__file__).resolve()), '--seed-worker', str(directory)], env),
                ([sys.executable, str(ROOT / 'scripts/rehearse_postgres.py'), '--sqlite-source', str(directory / 'synthetic-source.sqlite3'), '--source-media', str(directory / 'media'), '--new-directory', str(directory / 'rehearsal')], os.environ.copy())]
    for index, (command, child_env) in enumerate(commands):
        with (directory / f'step-{index}.log').open('w') as log:
            result = subprocess.run(command, env=child_env, stdout=log, stderr=log)
        if result.returncode:
            print(json.dumps({'status': 'FAILED', 'step': index, 'private_artifacts': str(directory)}))
            return result.returncode
    report = json.loads((directory / 'rehearsal/result.json').read_text())
    assert report['transfer']['sequences']['content_topic'] == 9000
    assert report['transfer']['sequences']['auth_user_groups'] == 9001
    assert report['transfer']['tables']['content_quizattempt_incorrect_questions']['count'] == 2
    for table in ['content_tag', 'content_topicalias', 'content_topic_tags', 'content_topicpublication_tags', 'content_question_related_topics', 'content_question_tags', 'content_connectionscan', 'content_keywordlinkproposal', 'content_studentidentity', 'content_authratewindow', 'content_studyplan', 'content_studyplan_selected_topics', 'content_studytask']:
        assert report['transfer']['tables'][table]['count'] > 0, table
    print(json.dumps({'status': 'PASS', 'private_artifacts': str(directory), 'postgres_database': report['postgres_database'],
                      'tables_compared': len(report['transfer']['tables']), 'rows_transferred': report['transfer']['rows'],
                      'deleted_id_counters_preserved': True, 'framework_and_m2m_ids_preserved': True, 'media_files_verified': report['backup_restore']['media_verified']}))
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--seed-worker':
        seed_worker(sys.argv[2])
    else:
        sys.exit(main())
