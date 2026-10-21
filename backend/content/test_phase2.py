"""Editorial acceptance and integrity regressions; synthetic, no external services."""
import hashlib
import json
from unittest import skipUnless
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import connection, IntegrityError, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase, SimpleTestCase
from django.urls import reverse
from .models import Tag, TopicAlias, Topic, TopicPublication, TopicRelation, ContentBlock, Quiz, Question, Choice, QuizReview, QuizAttempt
from .forms import QuestionForm
from .services.publication import publish, republish_previous, visible_publications
from .services.quiz import review_quiz, select_reviewed_quiz, QuizServiceError, quiz_fingerprint
from .services.collections import question_collection


class ContentFoundationTests(TestCase):
    def setUp(self):
        # SQLite's model-only runner does not create persistent content types;
        # clear manager entries referring to rolled-back prior TestCase rows.
        from django.contrib.contenttypes.models import ContentType
        ContentType.objects.clear_cache()
        self.editor = get_user_model().objects.create_superuser('phase2-editor', password='synthetic-only')
        self.root = Topic.objects.create(title='Subject', slug='phase2-subject')
        self.topic = Topic.objects.create(title='Primary lesson', slug='phase2-primary', parent=self.root)
        self.other = Topic.objects.create(title='Related lesson', slug='phase2-related', parent=self.root)
        self.block = ContentBlock.objects.create(topic=self.topic, block_type='text', content='<h2>Evidence</h2><p>Supported notes.</p>', source_reference='Synthetic source', order=1)
        for topic in (self.root, self.topic, self.other):
            publish(topic, self.editor)
        self.quiz = Quiz.objects.create(topic=self.topic, title='Reviewed fixture')
        self.q = Question.objects.create(quiz=self.quiz, question_text='Which statement is supported?', explanation='The source supports the first statement.')
        Choice.objects.create(question=self.q, choice_text='Supported', is_correct=True)
        Choice.objects.create(question=self.q, choice_text='Unsupported')
        review_quiz(self.quiz, self.editor, 'Synthetic reference')
        self.client.force_login(self.editor)

    def test_tag_normalization_uniqueness_and_stable_slug(self):
        tag = Tag.objects.create(name='  ＲＰＳＣ   History  ')
        self.assertEqual(tag.normalized_name, 'rpsc history')
        self.assertEqual(tag.slug, 'rpsc-history')
        with self.assertRaises(ValidationError):
            Tag.objects.create(name='rpsc HISTORY')
        with self.assertRaises(ValidationError):
            Tag.objects.create(name='Another', slug=tag.slug)
        old_slug = tag.slug
        tag.name = 'Revised history'; tag.save()
        self.assertEqual(tag.slug, old_slug)
        self.assertEqual(Tag.objects.get(pk=tag.pk).normalized_name, 'revised history')
        hindi = Tag.objects.create(name='राजस्थान इतिहास')
        self.assertTrue(hindi.slug)
        with self.assertRaises(ValidationError): Tag.objects.create(name='   ')
        tag.name = 'Partial update'; tag.save(update_fields=['name']); tag.refresh_from_db()
        self.assertEqual(tag.normalized_name, 'partial update')
        with self.assertRaises(ValidationError): Tag.objects.create(name='ß' * 100)

    def test_database_uniqueness_is_not_only_a_form_check(self):
        Tag.objects.create(name='Controlled')
        with self.assertRaises(IntegrityError), transaction.atomic():
            Tag.objects.bulk_create([Tag(name='Other', normalized_name='controlled', slug='other')])

    def test_aliases_are_controlled_unambiguous_and_id_based(self):
        alias = TopicAlias.objects.create(topic=self.topic, name='  SOURCE   Studies ')
        self.assertEqual(alias.status, 'draft')
        with self.assertRaises(ValidationError):
            TopicAlias.objects.create(topic=self.other, name='source studies')
        alias.status = 'approved'; alias.save()
        self.topic.title = 'Renamed'; self.topic.slug = 'renamed-draft'; self.topic.save()
        alias.refresh_from_db()
        self.assertEqual(alias.topic_id, self.topic.pk)
        self.assertEqual(alias.status, 'approved')
        # Alias registration does not implement discovery or automatic links.
        self.assertEqual(self.client.get('/api/search/?q=source%20studies').json()['results'], [])

    def test_publication_tags_are_explicit_and_frozen_until_publish(self):
        tag = Tag.objects.create(name='Evidence')
        self.topic.tags.add(tag)
        pub = TopicPublication.objects.get(topic=self.topic)
        self.assertFalse(pub.tags.exists())
        pub = publish(self.topic, self.editor)
        self.assertEqual(list(pub.tags.values_list('pk', flat=True)), [tag.pk])
        self.assertEqual(pub.snapshot['tags'][0]['id'], tag.pk)
        self.topic.tags.clear()
        self.assertTrue(pub.tags.filter(pk=tag.pk).exists())
        pub = publish(self.topic, self.editor)
        self.assertFalse(pub.tags.exists())
        republish_previous(pub, self.editor)
        self.assertTrue(pub.tags.filter(pk=tag.pk).exists())

    def test_relationship_review_and_withdrawal_gate_existing_snapshots(self):
        rel = TopicRelation.objects.create(source=self.topic, target=self.other, kind='related', reason='Evidence connection')
        publish(self.topic, self.editor)
        self.assertEqual(visible_publications()[self.topic.pk].snapshot['relations'], [])
        rel.status = 'approved'; rel.save(); publish(self.topic, self.editor)
        self.assertEqual(visible_publications()[self.topic.pk].snapshot['relations'][0]['target_id'], self.other.pk)
        self.other.title = 'Renamed related'; self.other.save()
        rel.refresh_from_db(); self.assertEqual(rel.target_id, self.other.pk)
        rel.status = 'withdrawn'; rel.save()
        self.assertEqual(visible_publications()[self.topic.pk].snapshot['relations'], [])

    def test_invalid_relationships_are_rejected_by_admin_forms(self):
        response = self.client.post('/admin/content/topicrelation/add/', {'source':self.topic.pk, 'target':self.topic.pk, 'kind':'related', 'reason':'Invalid', 'status':'approved', '_save':'Save'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A topic cannot relate to itself.')
        self.assertFalse(TopicRelation.objects.exists())

    def test_content_create_edit_preview_review_publish_withdraw(self):
        url = reverse('admin:content_contentblock_add')
        response = self.client.post(url, {'topic':self.topic.pk, 'block_type':'text', 'order':2, 'content':'<h3>Draft evidence</h3><p>Body</p><script>window.pwned=1</script>', 'source_reference':'Synthetic reference', '_save':'Save'})
        self.assertEqual(response.status_code, 302)
        block = ContentBlock.objects.get(topic=self.topic, order=2)
        self.assertEqual(TopicPublication.objects.get(topic=self.topic).revision, 1)
        preview = self.client.get(reverse('admin:content_topic_preview', args=[self.topic.pk]))
        self.assertContains(preview, '<h3>Draft evidence</h3>', html=True)
        self.assertNotContains(preview, 'window.pwned')
        change = reverse('admin:content_contentblock_change', args=[block.pk])
        response = self.client.post(change, {'topic':self.topic.pk, 'block_type':'text', 'order':2, 'content':'<p>Edited draft</p>', 'source_reference':'Synthetic reference', '_save':'Save'})
        self.assertEqual(response.status_code, 302)
        topic_url = reverse('admin:content_topic_change', args=[self.topic.pk])
        self.client.post(topic_url, {'_submit_review':'1'})
        self.topic.refresh_from_db(); self.assertEqual(self.topic.editorial_status, 'in_review')
        self.assertEqual(TopicPublication.objects.get(topic=self.topic).revision, 1)
        response = self.client.post(topic_url, {'_publish_now':'1'}, follow=True)
        self.assertContains(response, 'Published')
        self.assertContains(self.client.get('/api/topic/phase2-primary/'), 'Edited draft')
        self.client.post(topic_url, {'_withdraw_now':'1'})
        self.assertNotContains(self.client.get('/api/topic/phase2-primary/'), 'Edited draft')
        self.assertTrue(ContentBlock.objects.filter(pk=block.pk).exists())

    def test_publication_rejects_missing_references_without_replacing_live_notes(self):
        self.block.source_reference = ''; self.block.content = '<p>Unreviewed edit</p>'; self.block.save()
        response = self.client.post(reverse('admin:content_topic_change', args=[self.topic.pk]), {'_publish_now':'1'}, follow=True)
        self.assertContains(response, 'source references')
        self.assertEqual(TopicPublication.objects.get(topic=self.topic).revision, 1)
        self.assertNotContains(self.client.get('/api/topic/phase2-primary/'), 'Unreviewed edit')

    def test_tag_and_alias_admin_save_validation(self):
        self.assertEqual(self.client.post('/admin/content/tag/add/', {'name':'  Field   study ', 'slug':'', '_save':'Save'}).status_code, 302)
        response = self.client.post('/admin/content/tag/add/', {'name':'FIELD STUDY', 'slug':'different', '_save':'Save'})
        self.assertContains(response, 'normalized name already exists')
        self.assertEqual(Tag.objects.count(), 1)
        response = self.client.post('/admin/content/topicalias/add/', {'topic':self.topic.pk, 'name':'Evidence source', 'status':'draft', '_save':'Save'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TopicAlias.objects.get().status, 'draft')
        response = self.client.post('/admin/content/topicalias/add/', {'topic':999999, 'name':'Invalid target', 'status':'approved', '_save':'Save'})
        self.assertContains(response, 'Select a valid choice')
        response = self.client.post('/admin/content/tag/add/', {'name':'ß' * 100, 'slug':'expanded', '_save':'Save'})
        self.assertContains(response, 'normalized tag name must fit')

    def test_question_associations_and_distinct_subject_collection(self):
        self.q.related_topics.add(self.other)
        tag = Tag.objects.create(name='Sources'); self.q.tags.add(tag)
        self.assertEqual(list(question_collection(self.root, reviewed_only=False).values_list('pk', flat=True)), [self.q.pk])
        self.assertEqual(list(question_collection(self.other, reviewed_only=False).values_list('pk', flat=True)), [self.q.pk])
        self.assertFalse(question_collection(self.root).exists())  # Changed metadata needs review.
        review_quiz(self.quiz, self.editor, 'Synthetic reference')
        self.assertEqual(list(question_collection(self.root).values_list('pk', flat=True)), [self.q.pk])
        self.assertEqual(Question.objects.count(), 1)
        response = self.client.get('/admin/content/question/', {'collection':self.root.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cl'].result_count, 1)
        self.assertEqual(QuizAttempt.objects.count(), 0)
        TopicPublication.objects.filter(topic=self.other).update(is_published=False)
        self.assertFalse(question_collection(self.other).exists())
        self.assertTrue(question_collection(self.other, reviewed_only=False).exists())

    def test_question_admin_validates_primary_and_related_locations(self):
        data = {'quiz':self.quiz.pk, 'question_text':'Source question', 'explanation':'Reason', 'primary_topic':self.topic.pk, 'related_topics':[self.topic.pk]}
        form = QuestionForm(data=data, instance=self.q)
        self.assertFalse(form.is_valid()); self.assertIn('must not also', str(form.errors))
        data['primary_topic'] = self.root.pk; data['related_topics'] = []
        form = QuestionForm(data=data, instance=self.q)
        self.assertFalse(form.is_valid()); self.assertIn('leaf subtopic', str(form.errors))
        data['primary_topic'] = self.topic.pk; data['related_topics'] = [self.other.pk]
        form = QuestionForm(data=data, instance=self.q)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(Question.objects.get(pk=self.q.pk).primary_topic_id, self.topic.pk)
        self.assertEqual(list(self.q.related_topics.all()), [self.other])

    def test_legacy_approval_survives_backfill_but_metadata_edits_require_review(self):
        select_reviewed_quiz(self.topic.slug, self.quiz.pk)
        from django.db.models import Prefetch
        reversed_quiz = Quiz.objects.prefetch_related(Prefetch('questions', queryset=Question.objects.order_by('-pk').prefetch_related(Prefetch('choices', queryset=Choice.objects.order_by('-pk'))))).get(pk=self.quiz.pk)
        self.assertEqual(quiz_fingerprint(self.quiz), quiz_fingerprint(reversed_quiz))
        self.q.related_topics.add(self.other)
        with self.assertRaises(QuizServiceError): select_reviewed_quiz(self.topic.slug, self.quiz.pk)
        review_quiz(self.quiz, self.editor, 'Synthetic reference')
        select_reviewed_quiz(self.topic.slug, self.quiz.pk)
        self.other.title = 'Retitled'; self.other.save()
        select_reviewed_quiz(self.topic.slug, self.quiz.pk)
        self.assertEqual(QuizAttempt.objects.count(), 0)
        self.q.related_topics.add(self.topic)
        with self.assertRaises(QuizServiceError): review_quiz(self.quiz, self.editor, 'Synthetic reference')

    def test_editorial_navigation_permissions_and_maintenance_boundaries(self):
        staff = get_user_model().objects.create_user('phase2-staff', is_staff=True)
        names = ['topic', 'contentblock', 'question', 'quiz', 'tag', 'topicalias', 'topicrelation', 'learningresource', 'resourcepage', 'quizreview']
        from django.contrib.contenttypes.models import ContentType
        for name in names:
            ct, _ = ContentType.objects.get_or_create(app_label='content', model=name)
            for action in ['view', 'add', 'change']:
                permission, _ = Permission.objects.get_or_create(content_type=ct, codename=f'{action}_{name}', defaults={'name':f'Can {action} {name}'})
                staff.user_permissions.add(permission)
        self.client.force_login(staff)
        response = self.client.get('/admin/')
        for name in ['Topics', 'Content', 'Practice Questions']:
            self.assertContains(response, name)
        self.assertNotContains(response, 'Advanced maintenance')
        for url in ['/admin/content/resourcepage/', '/admin/content/quizreview/']:
            self.assertEqual(self.client.get(url).status_code, 403)
        self.assertEqual(self.client.get('/admin/content/tag/add/').status_code, 200)
        staff.user_permissions.clear(); staff = get_user_model().objects.get(pk=staff.pk)
        self.client.force_login(staff)
        self.assertEqual(self.client.get('/admin/content/tag/add/').status_code, 403)
        self.assertEqual(self.client.get('/admin/content/topic/tree/').status_code, 403)


@skipUnless(connection.vendor == 'postgresql', 'Real migration graph requires disposable PostgreSQL')
class Phase2MigrationTests(TransactionTestCase):
    def test_forward_reverse_preserves_legacy_ids_rows_reviews_and_learner_data(self):
        before = ('content', '0006_learner_ownership')
        latest = ('content', '0007_tag_question_primary_topic_question_related_topics_and_more')
        executor = MigrationExecutor(connection)
        restore_targets = executor.loader.graph.leaf_nodes()
        executor.migrate([before])
        old = executor.loader.project_state([before]).apps
        try:
            topic = old.get_model('content', 'Topic').objects.create(title='Legacy topic', slug='legacy-phase2')
            target = old.get_model('content', 'Topic').objects.create(title='Legacy related', slug='legacy-related')
            draft = old.get_model('content', 'Topic').objects.create(title='Never reviewed', slug='legacy-draft')
            relation = old.get_model('content', 'TopicRelation').objects.create(source_id=topic.pk, target_id=target.pk, kind='related', reason='Reviewed connection')
            pending = old.get_model('content', 'TopicRelation').objects.create(source_id=topic.pk, target_id=draft.pk, kind='related', reason='Unreviewed')
            old.get_model('content', 'TopicPublication').objects.create(topic_id=topic.pk, title=topic.title, is_published=True, snapshot={'slug':topic.slug, 'parent_id':None, 'blocks':[], 'relations':[{'target_id':target.pk, 'kind':'related', 'reason':relation.reason}]})
            quiz = old.get_model('content', 'Quiz').objects.create(topic_id=topic.pk, title='Legacy practice')
            q = old.get_model('content', 'Question').objects.create(quiz_id=quiz.pk, question_text='Preserved?', explanation='Yes')
            old.get_model('content', 'Choice').objects.create(question_id=q.pk, choice_text='Yes', is_correct=True)
            old.get_model('content', 'Choice').objects.create(question_id=q.pk, choice_text='No', is_correct=False)
            attempt = old.get_model('content', 'QuizAttempt').objects.create(quiz_id=quiz.pk, score=1, total_questions=1)
            old.get_model('content', 'QuizAttempt').objects.get(pk=attempt.pk).incorrect_questions.add(q.pk)
            bookmark = old.get_model('content', 'Bookmark').objects.create(topic_id=topic.pk)
            progress = old.get_model('content', 'UserProgress').objects.create(topic_id=topic.pk, is_completed=True)
            legacy = [quiz.pk, quiz.title, topic.pk, [[q.pk, q.question_text, q.explanation, list(old.get_model('content', 'Choice').objects.filter(question_id=q.pk).order_by('pk').values_list('pk', 'choice_text', 'is_correct'))]]]
            fingerprint = hashlib.sha256(json.dumps(legacy, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
            old.get_model('content', 'QuizReview').objects.create(quiz_id=quiz.pk, is_approved=True, fingerprint=fingerprint, source_reference='Legacy source')
            for _ in range(2):
                executor = MigrationExecutor(connection); executor.migrate([latest])
                current = Question.objects.get(pk=q.pk)
                self.assertEqual(current.primary_topic_id, topic.pk)
                state = MigrationExecutor(connection).loader.project_state([latest]).apps
                self.assertEqual(quiz_fingerprint(state.get_model('content', 'Quiz').objects.get(pk=quiz.pk)), fingerprint)
                self.assertEqual(QuizReview.objects.get(quiz_id=quiz.pk).fingerprint, fingerprint)
                self.assertEqual(TopicRelation.objects.get(pk=relation.pk).status, 'approved')
                self.assertEqual(TopicRelation.objects.get(pk=pending.pk).status, 'draft')
                self.assertEqual(QuizAttempt.objects.get(pk=attempt.pk).incorrect_questions.get().pk, q.pk)
                from .models import Bookmark, UserProgress
                self.assertEqual(Bookmark.objects.get(pk=bookmark.pk).topic_id, topic.pk)
                self.assertTrue(UserProgress.objects.get(pk=progress.pk).is_completed)
                executor = MigrationExecutor(connection); executor.migrate([before])
                self.assertEqual(old.get_model('content', 'Question').objects.get(pk=q.pk).question_text, 'Preserved?')
        finally:
            MigrationExecutor(connection).migrate(restore_targets)


class SQLiteMigrationTests(SimpleTestCase):
    def test_disposable_sqlite_roundtrip_preserves_deleted_id_high_water_marks(self):
        import os
        import subprocess
        import sys
        from pathlib import Path
        from tempfile import TemporaryDirectory
        code = r"""
import django
django.setup()
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
before = ('content', '0006_learner_ownership')
latest = ('content', '0007_tag_question_primary_topic_question_related_topics_and_more')
e = MigrationExecutor(connection); e.migrate([before]); apps = e.loader.project_state([before]).apps
Topic = apps.get_model('content', 'Topic'); Quiz = apps.get_model('content', 'Quiz'); Question = apps.get_model('content', 'Question')
t = Topic.objects.create(title='Synthetic', slug='sqlite-roundtrip')
qz = Quiz.objects.create(topic_id=t.pk, title='Synthetic')
q = Question.objects.create(quiz_id=qz.pk, question_text='Retained canonical question', explanation='Retained')
Topic.objects.create(pk=9000, title='Deleted fixture', slug='deleted-fixture').delete()
Question.objects.create(pk=9001, quiz_id=qz.pk, question_text='Deleted fixture').delete()
for target in [latest, before, latest]:
    MigrationExecutor(connection).migrate([target])
    with connection.cursor() as c:
        for table, expected in [('content_topic',9000), ('content_question',9001)]:
            c.execute('SELECT seq FROM sqlite_sequence WHERE name=%s',[table]); assert c.fetchone()[0] == expected
    current = MigrationExecutor(connection).loader.project_state([target]).apps
    assert current.get_model('content','Question').objects.get(pk=q.pk).question_text == 'Retained canonical question'
    if target == latest: assert current.get_model('content','Question').objects.get(pk=q.pk).primary_topic_id == t.pk
"""
        with TemporaryDirectory(prefix='prepal-phase2-migration-') as directory:
            env = {**os.environ, 'DJANGO_SETTINGS_MODULE':'core.settings', 'PYTHON_DOTENV_DISABLED':'1',
                   'DATABASE_ENGINE':'sqlite', 'DATABASE_PATH':str(Path(directory) / 'synthetic.sqlite3'),
                   'DJANGO_ENV':'development', 'AI_ENABLED':'false', 'AI_GUEST_ENABLED':'false',
                   'GEMINI_API_KEY':'', 'GOOGLE_API_KEY':''}
            result = subprocess.run([sys.executable, '-c', code], cwd=Path(__file__).resolve().parents[1], env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr[-2500:])
