from tempfile import TemporaryDirectory
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient
from .models import Topic, ContentBlock, TopicPublication, TopicRelation, Quiz, Question, Choice, QuizAttempt, LearningResource, AiBudgetBucket, AiRequest
from .services.publication import publish, republish_previous, sanitize
from .services.quiz import review_quiz
from .services.resources import process_resource, approve_resource
from .services.retrieval import DatabaseRetrievalProvider
from .services.ai_budget import reserve, finish
from .exceptions import ServiceError
from .management.commands.create_demo import demo_pdf


class ProductTests(TestCase):
    def setUp(self):
        self.editor = get_user_model().objects.create_superuser('editor-fixture', password='test-only')
        self.parent = Topic.objects.create(title='Reviewed fixture collection', slug='collection')
        self.topic = Topic.objects.create(title='Observation fixture', slug='observation', parent=self.parent)
        self.related = Topic.objects.create(title='Sequence fixture', slug='sequence', parent=self.parent)
        self.block = ContentBlock.objects.create(topic=self.topic, block_type='text', content='<h2>Observe carefully</h2><p>Observation describes evidence. Inference needs support.</p>', source_reference='Synthetic source', order=1)
        ContentBlock.objects.create(topic=self.related, block_type='text', content='<p>A sequence orders events.</p>', source_reference='Synthetic source', order=1)
        publish(self.parent, self.editor); publish(self.topic, self.editor); publish(self.related, self.editor)
        self.quiz = Quiz.objects.create(topic=self.topic, title='Reviewed fixture practice')
        self.q = Question.objects.create(quiz=self.quiz, question_text='What describes evidence?', explanation='An observation describes evidence.')
        self.correct = Choice.objects.create(question=self.q, choice_text='Observation', is_correct=True)
        self.wrong = Choice.objects.create(question=self.q, choice_text='A guess')
        review_quiz(self.quiz, self.editor, 'Synthetic source')

    def test_draft_edits_cannot_leak_through_catalog_reader_search_or_retrieval(self):
        self.topic.title = 'PRIVATE TITLE'; self.topic.save()
        self.block.content = 'PRIVATE DRAFT SECRET'; self.block.save()
        for url in ['/api/topics/?tree=1', '/api/topic/observation/', '/api/search/?q=PRIVATE']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('PRIVATE', response.content.decode())
        _, evidence = DatabaseRetrievalProvider().retrieve('observation', {'message': 'Observation'})
        self.assertTrue(evidence); self.assertNotIn('PRIVATE', str(evidence))

    def test_withdrawn_ancestor_hides_descendants_and_quizzes(self):
        TopicPublication.objects.filter(topic=self.parent).update(is_published=False)
        self.assertEqual(self.client.get('/api/topics/?published_only=1').json(), [])
        topics = self.client.get('/api/topics/').json()
        self.assertEqual(len(topics), 1)
        self.assertFalse(topics[0]['is_published'])
        self.assertFalse(topics[0]['has_notes'])
        detail = self.client.get('/api/topic/observation/').json()
        self.assertFalse(detail['has_notes'])
        self.assertEqual(detail['blocks'], [])
        self.assertEqual(detail['status'], 'coming_soon')
        self.assertEqual(self.client.get('/api/topic/observation/quiz/').status_code, 404)
        self.assertEqual(self.client.get('/api/search/?q=Observation').json()['results'], [])

    def test_publishing_and_previous_snapshot_are_explicit(self):
        self.block.content = '<p>New reviewed material.</p>'; self.block.save()
        pub = publish(self.topic, self.editor)
        self.assertIn('New reviewed', self.client.get('/api/topic/observation/').content.decode())
        revision = pub.revision; republish_previous(pub, self.editor)
        self.assertGreater(pub.revision, revision)
        self.assertIn('Observation describes', self.client.get('/api/topic/observation/').content.decode())

    def test_related_scope_requires_explicit_published_edge_and_request(self):
        TopicRelation.objects.create(source=self.topic, target=self.related, kind='related', status='approved', reason='Fixture connection')
        _, before = DatabaseRetrievalProvider().retrieve('observation', {'message': 'sequence', 'allow_related': True})
        self.assertEqual(before, [])
        publish(self.topic, self.editor)
        _, denied = DatabaseRetrievalProvider().retrieve('observation', {'message': 'sequence'})
        _, allowed = DatabaseRetrievalProvider().retrieve('observation', {'message': 'sequence', 'allow_related': True})
        self.assertEqual(denied, []); self.assertTrue(allowed)
        self.assertEqual({e['topic_id'] for e in allowed}, {self.related.pk})

    def test_selection_requires_current_source_text_and_revision(self):
        for selected in [{'source_id': 'b9999', 'text': 'invented', 'revision': 1}, {'source_id': f'b{self.block.pk}', 'text': 'injected unrelated text', 'revision': 1}, {'source_id': f'b{self.block.pk}', 'text': 'Observation', 'revision': 999}]:
            with self.assertRaises(ServiceError): DatabaseRetrievalProvider().retrieve('observation', {'message': 'Explain', 'selected': selected})

    def test_search_input_and_publication_sanitizer(self):
        self.assertEqual(self.client.get('/api/search/', {'q': 'x'*201}).status_code, 400)
        self.assertEqual(self.client.get('/api/search/', {'page': '9'*5000}).status_code, 400)
        self.assertEqual(self.client.get('/api/search/', {'q': 'Observation', 'page': '-1'}).status_code, 400)
        clean = sanitize('<h2>Heading</h2><table><tr><td>Fact</td></tr></table><script>alert(1)</script><img onerror=x src=x><iframe src=x></iframe><a href="javascript:alert(1)">Bad</a>')
        self.assertIn('<table>', clean)
        for token in ['<script', '<img', '<iframe', 'javascript:', 'onerror']: self.assertNotIn(token, clean)

    def test_quiz_check_is_deterministic_read_only_and_detects_content_edits(self):
        preview = self.client.get('/api/topic/observation/quiz/').json()
        self.assertNotIn('is_correct', str(preview))
        payload = {'quiz_id': self.quiz.pk, 'revision_token': preview['revision_token'], 'answers': {str(self.q.pk): self.correct.pk}}
        with CaptureQueriesContext(connection) as queries:
            first = self.client.post('/api/topic/observation/quiz/check/', payload, content_type='application/json')
            second = self.client.post('/api/topic/observation/quiz/check/', payload, content_type='application/json')
        self.assertEqual(first.status_code, 200); self.assertEqual(first.json(), second.json()); self.assertEqual(first.json()['score'], 1)
        self.assertEqual(QuizAttempt.objects.count(), 0)
        self.assertFalse(any(q['sql'].lstrip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')) for q in queries))
        self.q.explanation = 'Edited explanation'; self.q.save()
        self.assertEqual(self.client.get('/api/topic/observation/quiz/').status_code, 404)
        review_quiz(self.quiz, self.editor, 'Re-reviewed source')
        self.assertEqual(self.client.post('/api/topic/observation/quiz/check/', payload, content_type='application/json').status_code, 409)

    def test_guest_write_contract_requires_csrf_but_legacy_submit_stays_constant(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertEqual(client.post('/api/topic/observation/quiz/check/', {}, format='json').status_code, 403)
        self.assertEqual(client.post('/api/topic/observation/chat/', {'message': 'Explain'}, format='json').status_code, 403)
        self.assertEqual(client.post('/api/topic/observation/quiz/submit/', {}, format='json').status_code, 503)

        config = client.get('/api/config/').json(); preview = client.get('/api/topic/observation/quiz/').json()
        response = client.post('/api/topic/observation/quiz/check/', {'quiz_id': self.quiz.pk, 'revision_token': preview['revision_token'], 'answers': {}}, format='json', HTTP_X_CSRFTOKEN=config['csrf_token'])
        self.assertEqual(response.status_code, 200)

    def test_admin_preview_is_staff_only_sanitized_and_drafts_remain_private(self):
        self.block.content = '<p>Private preview</p><script>alert(1)</script>'; self.block.save()
        url = f'/admin/content/topic/{self.topic.pk}/preview/'
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.editor); response = self.client.get(url)
        self.assertContains(response, 'Private preview'); self.assertNotIn('<script>alert(1)</script>', response.content.decode())
        self.assertNotIn('Private preview', self.client.get('/api/topic/observation/').content.decode())

    @override_settings(AI_ENABLED=True, AI_GUEST_ENABLED=True, AI_MODEL='fixture-model', GEMINI_API_KEY='fixture-only', AI_DAILY_BUDGET_MICRO=100000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000)
    def test_tutor_validates_citations_and_never_calls_provider_without_evidence(self):
        self.client.get('/api/config/'); payload = {'message': 'Observation'}
        valid = {'answer': 'Observation describes evidence.', 'citations': [f'b{self.block.pk}'], 'insufficient': False}
        with patch('content.services.providers.GeminiProvider.generate', return_value=(valid, None)) as provider:
            result = self.client.post('/api/topic/observation/chat/', payload, content_type='application/json')
            self.assertEqual(result.status_code, 200); self.assertTrue(result.json()['citations'][0]['url'].startswith('/topic/observation#'))
            unsupported = self.client.post('/api/topic/observation/chat/', {'message': 'quasar spectroscopy'}, content_type='application/json')
            self.assertEqual(unsupported.json()['status'], 'insufficient_context'); self.assertEqual(provider.call_count, 1)
        with patch('content.services.providers.GeminiProvider.generate', return_value=({'answer': 'Invented', 'citations': ['bad'], 'insufficient': False}, None)):
            self.assertEqual(self.client.post('/api/topic/observation/chat/', payload, content_type='application/json').status_code, 502)
        with patch('content.services.providers.GeminiProvider.generate', side_effect=TimeoutError('private diagnostics')):
            response = self.client.post('/api/topic/observation/chat/', payload, content_type='application/json')
            self.assertEqual(response.status_code, 503); self.assertNotIn('private diagnostics', response.content.decode())

    @override_settings(AI_DAILY_BUDGET_MICRO=5000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000, AI_MODEL='fixture-model')
    def test_budget_reserves_conservatively_and_rollback_does_not_partially_charge(self):
        first = reserve('visitor', 'ip', 1000)
        with self.assertRaises(ServiceError): reserve('visitor', 'ip', 1000)
        self.assertEqual(AiRequest.objects.count(), 1); finish(first)
        self.assertEqual(AiBudgetBucket.objects.get(key__startswith='global:').reserved_micro, 2000)
        other = reserve('another', 'ip', 1000); finish(other, 1000)
        third = reserve('third', 'ip', 1000); finish(third)
        with self.assertRaises(ServiceError): reserve('fourth', 'ip', 1)
        self.assertEqual(AiBudgetBucket.objects.get(key__startswith='global:').reserved_micro, 5000)

    def test_pdf_ingestion_review_publication_search_and_withdrawal(self):
        with TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory, STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'}, 'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}}):
            resource = LearningResource(topic=self.topic, title='Fixture field guide', source_reference='Original fixture', rights_note='Original synthetic text')
            resource.file.save('fixture.pdf', ContentFile(demo_pdf('Fixture reading guide')), save=True)
            self.assertEqual(self.client.get(f'/api/resources/{resource.pk}/file/').status_code, 404)
            self.assertTrue(process_resource(resource.pk)); resource.refresh_from_db()
            self.assertEqual(resource.status, 'ready'); self.assertEqual(resource.page_count, 2)
            approve_resource(resource, self.editor)
            self.assertEqual(self.client.get(f'/api/resources/{resource.pk}/').status_code, 404)
            publish(self.topic, self.editor)
            result = self.client.get(f'/api/resources/{resource.pk}/?page=2')
            self.assertEqual(result.status_code, 200); self.assertIn('Observation', result.json()['text'])
            download = self.client.get(f'/api/resources/{resource.pk}/file/')
            self.assertEqual(download.status_code, 200); self.assertEqual(b''.join(download.streaming_content)[:5], b'%PDF-')
            self.assertTrue(any(r['kind'] == 'pdf' for r in self.client.get('/api/search/?q=Observation').json()['results']))
            LearningResource.objects.filter(pk=resource.pk).update(status='withdrawn')
            self.assertEqual(self.client.get(f'/api/resources/{resource.pk}/file/').status_code, 404)
            self.assertFalse(any(r['kind'] == 'pdf' for r in self.client.get('/api/search/?q=Observation').json()['results']))

    def test_pdf_worker_recovers_missing_files_and_exhausted_claims(self):
        from datetime import timedelta
        from django.utils import timezone
        resource = LearningResource.objects.create(topic=self.topic, title='Missing fixture', file='does-not-exist.pdf', source_reference='Fixture', rights_note='Fixture')
        self.assertTrue(process_resource(resource.pk)); resource.refresh_from_db()
        self.assertEqual(resource.status, 'failed')
        resource.status = 'processing'; resource.attempts = 3; resource.processing_deadline = timezone.now() - timedelta(seconds=10); resource.save()
        self.assertFalse(process_resource(resource.pk)); resource.refresh_from_db()
        self.assertEqual(resource.status, 'failed'); self.assertEqual(resource.error_code, 'attempt_limit')

    @override_settings(AI_ENABLED=True, AI_GUEST_ENABLED=True, AI_MODEL='fixture-model', GEMINI_API_KEY='fixture-only', AI_DAILY_BUDGET_MICRO=100000, AI_INPUT_RATE_MICRO=1000000, AI_OUTPUT_RATE_MICRO=1000000)
    def test_tutor_rechecks_source_publication_after_provider_returns(self):
        self.client.get('/api/config/')
        def withdraw(*args):
            TopicPublication.objects.filter(topic=self.topic).update(is_published=False)
            return {'answer': 'Observation describes evidence.', 'citations': [f'b{self.block.pk}'], 'insufficient': False}, None
        with patch('content.services.providers.GeminiProvider.generate', side_effect=withdraw):
            self.assertEqual(self.client.post('/api/topic/observation/chat/', {'message': 'Observation'}, content_type='application/json').status_code, 409)

    def test_private_image_preview_and_public_storage_metadata_boundary(self):
        from io import BytesIO
        from PIL import Image
        with TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            buffer = BytesIO(); Image.new('RGB', (20, 20)).save(buffer, format='PNG')
            block = ContentBlock(topic=self.topic, block_type='image', order=10, alt_text='Synthetic square', source_reference='Original fixture')
            block.file.save('fixture.png', ContentFile(buffer.getvalue()), save=True)
            url = f'/admin/content/topic/{self.topic.pk}/draft-image/{block.pk}/'
            self.assertEqual(self.client.get(url).status_code, 302)
            self.client.force_login(self.editor); response = self.client.get(url)
            self.assertEqual(response.status_code, 200); self.assertTrue(b''.join(response.streaming_content))
            self.assertEqual(self.client.get(f'/api/topic/{self.topic.slug}/images/{block.pk}/').status_code, 404)
            publish(self.topic, self.editor)
            body = self.client.get(f'/api/topic/{self.topic.slug}/').json()
            self.assertNotIn('file_name', str(body)); self.assertNotIn('file_hash', str(body))
            response = self.client.get(f'/api/topic/{self.topic.slug}/images/{block.pk}/')
            self.assertEqual(response.status_code, 200); self.assertTrue(b''.join(response.streaming_content))

    @override_settings(AI_ENABLED=True, AI_GUEST_ENABLED=True, TRUSTED_PROXY_IPS=('127.0.0.1',))
    def test_proxy_identity_is_explicit_and_health_is_read_only(self):
        from django.utils.crypto import salted_hmac
        self.client.get('/api/config/')
        with patch('content.views.answer', return_value={'response': 'Mock', 'citations': []}) as mocked:
            self.assertEqual(self.client.post('/api/topic/observation/chat/', {'message': 'Observation'}, content_type='application/json', REMOTE_ADDR='127.0.0.1', HTTP_X_REAL_IP='203.0.113.9').status_code, 200)
            self.assertEqual(mocked.call_args.args[-1], salted_hmac('ip-quota', '203.0.113.9').hexdigest())
            self.client.post('/api/topic/observation/chat/', {'message': 'Observation'}, content_type='application/json', REMOTE_ADDR='203.0.113.8', HTTP_X_REAL_IP='203.0.113.9')
            self.assertEqual(mocked.call_args.args[-1], salted_hmac('ip-quota', '203.0.113.8').hexdigest())
            self.assertEqual(self.client.post('/api/topic/observation/chat/', {'message': 'Observation'}, content_type='application/json', REMOTE_ADDR='127.0.0.1', HTTP_X_REAL_IP='bad').status_code, 400)
        with CaptureQueriesContext(connection) as queries:
            self.assertEqual(self.client.get('/api/health/').json(), {'status': 'ok'})
        self.assertFalse(any(q['sql'].lstrip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')) for q in queries))

    def test_complete_syllabus_discovery_and_safe_coming_soon_notes(self):
        import json
        from pathlib import Path
        fixture_path = Path(__file__).resolve().parent / 'fixtures' / 'syllabus_142.json'
        if fixture_path.exists():
            with open(fixture_path) as f:
                raw_topics = json.load(f)
            # Create a detached branch of topics to verify complete tree loading
            test_root = Topic.objects.create(title='Rajasthan Official Syllabus', slug='rajasthan-official', order=100)
            child1 = Topic.objects.create(title='Pre-historical Sites', slug='pre-historical-sites', parent=test_root, order=1)
            subchild = Topic.objects.create(title='Palaeolithic Era', slug='palaeolithic-era', parent=child1, order=1)
            # Add draft block to subchild WITHOUT publishing it
            ContentBlock.objects.create(topic=subchild, block_type='text', content='<p>SECRET DRAFT UNAPPROVED</p>', order=1)

            # Test tree loading
            tree = self.client.get('/api/topics/?tree=1').json()
            found_root = next((t for t in tree if t['slug'] == 'rajasthan-official'), None)
            self.assertIsNotNone(found_root)
            self.assertTrue(found_root['has_children'])
            self.assertFalse(found_root['is_published'])
            self.assertFalse(found_root['has_notes'])

            # Test child in tree
            found_child = next((c for c in found_root['children'] if c['slug'] == 'pre-historical-sites'), None)
            self.assertIsNotNone(found_child)
            found_sub = next((s for s in found_child['children'] if s['slug'] == 'palaeolithic-era'), None)
            self.assertIsNotNone(found_sub)
            self.assertFalse(found_sub['has_notes'])

            # Test detail endpoint of unpublished topic: should return 200 with coming_soon, NOT 404
            detail = self.client.get('/api/topic/palaeolithic-era/').json()
            self.assertEqual(detail['status'], 'coming_soon')
            self.assertFalse(detail['has_notes'])
            self.assertEqual(detail['blocks'], [])  # Absolutely no draft content leaked!
            self.assertNotIn('SECRET', str(detail))
            self.assertEqual(len(detail['breadcrumbs']), 3)
            self.assertEqual(detail['breadcrumbs'][0]['slug'], 'rajasthan-official')
            self.assertEqual(detail['breadcrumbs'][1]['slug'], 'pre-historical-sites')
            self.assertEqual(detail['breadcrumbs'][2]['slug'], 'palaeolithic-era')

            # Test exact and typo-tolerant search across all discoverable syllabus topics
            search_res = self.client.get('/api/search/?q=Palaeolithic').json()
            self.assertEqual(len(search_res['results']), 1)
            self.assertEqual(search_res['results'][0]['title'], 'Palaeolithic Era')
            self.assertFalse(search_res['results'][0]['has_notes'])
            self.assertEqual(search_res['results'][0]['kind'], 'topic')
            self.assertEqual(search_res['results'][0]['url'], '/topic/palaeolithic-era')
            self.assertNotIn('SECRET', str(search_res))

            # Typo-tolerant search for "palaeothic" returns suggestions and matches
            typo_res = self.client.get('/api/search/?q=palaeothic').json()
            self.assertEqual(typo_res['suggestion'], 'palaeolithic')
            self.assertEqual(len(typo_res['results']), 1)
            self.assertEqual(typo_res['results'][0]['title'], 'Palaeolithic Era')
            self.assertNotIn('SECRET', str(typo_res))

