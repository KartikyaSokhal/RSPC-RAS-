"""Phase 3 editorial, publication, security and stateless discovery acceptance."""
from unittest.mock import patch
from unittest import skipUnless
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase, SimpleTestCase, override_settings
from django.test.utils import CaptureQueriesContext
from .models import Topic, ContentBlock, TopicPublication, TopicAlias, TopicRelation, Tag, KeywordLinkProposal, ConnectionScan, Quiz, Question, Choice, QuizAttempt
from .services.publication import publish, visible_publications
from .services.connections import suggest_connections, decide, find_matches, approved_links, process_pending
from .services.quiz import review_quiz
from .exceptions import ServiceError


class DiscoveryTests(TestCase):
    def setUp(self):
        ContentType.objects.clear_cache()
        self.editor = get_user_model().objects.create_superuser('discovery-editor', password='synthetic-only')
        self.root = Topic.objects.create(title='Synthetic Subject', slug='discovery-subject')
        self.source = Topic.objects.create(title='Sources and Claims', slug='discovery-source', parent=self.root)
        self.target = Topic.objects.create(title='Rajasthan History', slug='discovery-target', parent=self.root)
        self.short = Topic.objects.create(title='History', slug='discovery-short', parent=self.root)
        self.block = ContentBlock.objects.create(topic=self.source, block_type='text', order=1,
            content='<p>😀 RAJASTHAN HISTORY. Rajasthan History repeats. Historians use sources.</p>', source_reference='Synthetic reference')
        for t in [self.target, self.short]:
            ContentBlock.objects.create(topic=t, block_type='text', order=1, content='<p>Published evidence describes sources and chronology.</p>', source_reference='Synthetic reference')
        for t in [self.root, self.target, self.short, self.source]: publish(t, self.editor)
        self.client.force_login(self.editor)

    def proposals(self, status=None):
        rows = KeywordLinkProposal.objects.filter(source=self.source)
        return rows.filter(status=status) if status else rows

    def approve(self, target=None):
        p = self.proposals().filter(target=target or self.target).latest('pk'); decide(p, 'approved', self.editor); return p

    def test_case_insensitive_whole_phrase_unicode_and_overlaps(self):
        rows = list(find_matches('prehistory History Rajasthan HISTORY; राजस्थान इतिहासकार इतिहास; STRASSE', {'history':1,'rajasthan history':2,'इतिहास':3,'strasse':4}))
        self.assertEqual([target for _,target,_,_ in rows].count(1), 2)
        self.assertEqual([target for _,target,_,_ in rows].count(2), 1)
        self.assertEqual([target for _,target,_,_ in rows].count(3), 1)
        self.assertEqual([target for _,target,_,_ in rows].count(4), 1)
        self.assertNotIn('prehistory', [r[2]['text'] for r in rows])

    def test_proposals_pending_then_longest_approved_phrase_wins(self):
        self.assertEqual(approved_links(visible_publications()[self.source.pk], visible_publications()), [])
        for p in self.proposals(): decide(p, 'approved', self.editor)
        links = self.client.get('/api/topic/discovery-source/').json()['keyword_links']
        self.assertEqual(len(links), 1)  # History is only inside the longer phrases.
        self.assertEqual(links[0]['target_id'], self.target.pk)
        self.assertEqual(links[0]['start'], 3)  # Emoji = 2 UTF-16 units plus space.

    def test_count_limit_duplicate_prevention_and_no_self_links(self):
        content = '<p>Sources and Claims. ' + ' '.join(f'Concept {i} Concept {i}.' for i in range(12)) + '</p>'
        self.block.content = content; self.block.save()
        for i in range(12):
            t = Topic.objects.create(title=f'Concept {i}', slug=f'concept-{i}', parent=self.root)
            ContentBlock.objects.create(topic=t, block_type='text', order=1, content='<p>A synthetic approved concept explanation.</p>', source_reference='Synthetic')
            publish(t, self.editor)
        publish(self.source, self.editor)
        for p in self.proposals().filter(source_revision=TopicPublication.objects.get(topic=self.source).revision): decide(p, 'approved', self.editor)
        links = self.client.get('/api/topic/discovery-source/').json()['keyword_links']
        self.assertEqual(len(links), 8)
        self.assertEqual(len({l['target_id'] for l in links}), 8)
        self.assertNotIn(self.source.pk, {l['target_id'] for l in links})

    def test_decisions_survive_repeated_analysis_but_changed_html_needs_review(self):
        proposal = self.approve()
        rejected = self.proposals().get(target=self.short); decide(rejected, 'rejected', self.editor)
        count = self.proposals().count(); suggest_connections(self.source); suggest_connections(self.source)
        self.assertEqual(self.proposals().count(), count)
        proposal.refresh_from_db(); rejected.refresh_from_db()
        self.assertEqual(proposal.status, 'approved'); self.assertEqual(rejected.status, 'rejected')
        self.block.content = '<p>Different context: Rajasthan History supports a different claim.</p>'; self.block.save(); publish(self.source, self.editor)
        self.assertEqual(self.client.get('/api/topic/discovery-source/').json()['keyword_links'], [])
        self.assertTrue(self.proposals('pending').filter(target=self.target).exists())
        proposal.refresh_from_db(); self.assertEqual(proposal.status, 'approved')
        with self.assertRaises(ServiceError): decide(proposal, 'approved', self.editor)

    def test_drafts_withdrawal_and_alias_revocation_are_fail_closed(self):
        self.approve()
        TopicPublication.objects.filter(topic=self.target).update(is_published=False)
        data = self.client.get('/api/topic/discovery-source/').json()
        self.assertEqual(data['keyword_links'], [])
        self.assertNotIn(self.target.pk, {r['id'] for r in data['related']})
        publish(self.target, self.editor)
        self.assertTrue(self.client.get('/api/topic/discovery-source/').json()['keyword_links'])
        self.block.content='<p>Approved phrase</p>';self.block.save();publish(self.source,self.editor)
        alias=TopicAlias.objects.create(topic=self.target,name='Approved phrase',status='approved');process_pending()
        self.approve(); self.assertTrue(self.client.get('/api/topic/discovery-source/').json()['keyword_links'])
        alias.status='withdrawn';alias.save()
        self.assertEqual(self.client.get('/api/topic/discovery-source/').json()['keyword_links'], [])

    def test_new_topic_and_new_alias_queue_and_recheck_existing_articles(self):
        self.block.content='<p>A future concept and Additional vocabulary occur here.</p>';self.block.save();publish(self.source,self.editor)
        target=Topic.objects.create(title='Future concept',slug='future-concept',parent=self.root)
        ContentBlock.objects.create(topic=target,block_type='text',order=1,content='<p>New published evidence.</p>',source_reference='Synthetic')
        self.assertFalse(self.proposals().filter(target=target).exists())
        publish(target,self.editor)
        self.assertTrue(self.proposals('pending').filter(target=target).exists())
        self.client.post('/admin/content/topicalias/add/', {'topic':target.pk,'name':'Additional vocabulary','status':'approved','_save':'Save'})
        self.assertTrue(self.proposals('pending').filter(phrase_key='additional vocabulary',target=target).exists())
        self.assertEqual(self.client.get('/api/topic/discovery-source/').json()['keyword_links'], [])

    def test_existing_links_code_and_headings_are_not_annotated(self):
        self.block.content='<h2>Rajasthan History</h2><a href="https://example.org">Rajasthan History</a><pre>Rajasthan History</pre><p>A valid Rajasthan History phrase.</p>'
        self.block.save();publish(self.source,self.editor)
        proposal=self.proposals().filter(target=self.target).latest('pk')
        self.assertEqual(len(proposal.occurrences),1)

    def test_ambiguous_phrases_are_not_arbitrarily_linked(self):
        duplicate=Topic.objects.create(title=self.target.title,slug='ambiguous-target',parent=self.root)
        ContentBlock.objects.create(topic=duplicate,block_type='text',order=1,content='<p>Another published description.</p>',source_reference='Synthetic')
        self.approve();publish(duplicate,self.editor)
        self.assertEqual(self.client.get('/api/topic/discovery-source/').json()['keyword_links'], [])

    def test_reader_get_never_analyzes_or_writes_and_has_bounded_queries(self):
        self.approve();self.client.logout();before=list(KeywordLinkProposal.objects.values());html=self.block.content
        with patch('content.services.connections.compute_link_plan',side_effect=AssertionError('GET plan computation forbidden')), CaptureQueriesContext(connection) as queries:
            for _ in range(2): self.assertEqual(self.client.get('/api/topic/discovery-source/').status_code,200)
        self.assertLessEqual(len(queries),16)
        self.assertFalse(any(q['sql'].lstrip().upper().startswith(('INSERT','UPDATE','DELETE')) for q in queries))
        self.assertEqual(list(KeywordLinkProposal.objects.values()),before)
        self.block.refresh_from_db();self.assertEqual(self.block.content,html)

    def test_related_topics_deduplicate_filter_and_limit(self):
        TopicRelation.objects.create(source=self.source,target=self.target,kind='related',reason='Reviewed connection',status='approved')
        publish(self.source,self.editor)
        for i in range(8): publish(Topic.objects.create(title=f'Sibling {i}',slug=f'sibling-{i}',parent=self.root),self.editor)
        data=self.client.get('/api/topic/discovery-source/').json()['related']
        self.assertEqual(data[0]['id'],self.target.pk)
        self.assertEqual(len(data),6);self.assertEqual(len({r['id'] for r in data}),6)
        self.assertNotIn(self.source.pk,{r['id'] for r in data})

    def test_public_tags_use_released_associations_and_stable_slugs(self):
        tag=Tag.objects.create(name='Controlled History')
        self.source.tags.add(tag)
        self.assertEqual(self.client.get(f'/api/tags/{tag.slug}/').status_code,404)
        tag.is_public=True;tag.save()
        self.assertEqual(self.client.get(f'/api/tags/{tag.slug}/').json()['count'],0)
        publish(self.source,self.editor)
        response=self.client.get(f'/api/tags/{tag.slug}/').json()
        self.assertEqual(response['count'],1);self.assertTrue(response['results'][0]['syllabus_location']);self.assertGreater(response['results'][0]['read_minutes'],0)
        self.source.tags.clear();self.assertEqual(self.client.get(f'/api/tags/{tag.slug}/').json()['count'],1)
        TopicPublication.objects.filter(topic=self.source).update(is_published=False)
        self.assertEqual(self.client.get(f'/api/tags/{tag.slug}/').json()['results'],[])
        self.assertEqual(self.client.get('/api/tags/unknown/').status_code,404)
        self.assertEqual(self.client.get(f'/api/tags/{tag.slug}/?page=invalid').status_code,400)
        oldslug=tag.slug;tag.name='Renamed';tag.save();self.assertEqual(tag.slug,oldslug)
        tag.slug='unstable'
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):tag.save()

    def test_admin_suggestion_and_review_actions_check_permissions(self):
        response=self.client.post('/admin/content/topic/',{'action':'suggest_connections','_selected_action':[self.source.pk]},follow=True)
        self.assertContains(response,'connection proposals')
        proposal=self.proposals().filter(target=self.target).latest('pk')
        self.client.post('/admin/content/keywordlinkproposal/',{'action':'reject_connections','_selected_action':[proposal.pk]})
        proposal.refresh_from_db();self.assertEqual(proposal.status,'rejected')
        self.client.post('/admin/content/keywordlinkproposal/',{'action':'approve_connections','_selected_action':[proposal.pk]})
        proposal.refresh_from_db();self.assertEqual(proposal.reviewed_by,self.editor)
        staff=get_user_model().objects.create_user('no-review-permission',is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.post('/admin/content/keywordlinkproposal/',{'action':'approve_connections','_selected_action':[proposal.pk]}).status_code,403)

    def make_quiz(self,topic):
        quiz=Quiz.objects.create(topic=topic,title='Reviewed synthetic practice')
        q=Question.objects.create(quiz=quiz,question_text='Which claim has evidence?',explanation='The first claim is supported.')
        correct=Choice.objects.create(question=q,choice_text='Supported',is_correct=True)
        Choice.objects.create(question=q,choice_text='Unsupported')
        review_quiz(quiz,self.editor,'Synthetic source')
        return quiz,q,correct

    def test_dynamic_canonical_collections_and_stateless_grading(self):
        quiz,q,correct=self.make_quiz(self.source)
        q.related_topics.add(self.target);review_quiz(quiz,self.editor,'Synthetic source')
        path='/api/topic/discovery-subject/practice/'
        response=self.client.get(path);self.assertEqual(response.status_code,200)
        data=response.json();self.assertEqual([row['id'] for row in data['questions']],[q.pk])
        self.assertNotIn('is_correct',str(data))
        payload={'collection_id':self.root.pk,'page':1,'revision_token':data['revision_token'],'answers':{str(q.pk):correct.pk}}
        with CaptureQueriesContext(connection) as queries:
            results=[self.client.post(path+'check/',payload,content_type='application/json') for _ in range(2)]
        self.assertEqual([r.json()['score'] for r in results],[1,1])
        self.assertEqual(Question.objects.count(),1);self.assertEqual(Quiz.objects.count(),1);self.assertEqual(QuizAttempt.objects.count(),0)
        self.assertFalse(any(x['sql'].lstrip().upper().startswith(('INSERT','UPDATE','DELETE')) for x in queries))
        self.make_quiz(self.target);self.assertEqual(self.client.get(path).json()['count'],2)
        q.question_text='Changed question';q.save()
        self.assertNotEqual(self.client.post(path+'check/',payload,content_type='application/json').status_code,200)
        TopicPublication.objects.filter(topic=self.target).update(is_published=False)
        self.assertEqual(self.client.get(path).status_code,404)

    def test_collection_rejects_malformed_membership_tokens_and_csrf(self):
        quiz,q,correct=self.make_quiz(self.source);data=self.client.get('/api/topic/discovery-source/practice/').json()
        path='/api/topic/discovery-source/practice/check/'
        payload={'collection_id':self.source.pk,'page':1,'revision_token':data['revision_token'],'answers':{str(q.pk):correct.pk}}
        for change in [{'answers':[]},{'answers':{str(q.pk):True}},{'answers':{'999999':correct.pk}},{'answers':{str(q.pk):99999}},{'page':True},{'collection_id':self.target.pk},{'revision_token':'forged'}]:
            self.assertIn(self.client.post(path,{**payload,**change},content_type='application/json').status_code,(400,409))
        from rest_framework.test import APIClient
        guest=APIClient(enforce_csrf_checks=True)
        self.assertEqual(guest.post(path,payload,format='json').status_code,403)
        for query in ['?page=0','?page=1&page=2','?page=-1','?page=999999']:
            self.assertEqual(self.client.get('/api/topic/discovery-source/practice/'+query).status_code,400)
        self.assertEqual(self.client.get('/api/topic/discovery-short/practice/').status_code,404)
        self.assertEqual(QuizAttempt.objects.count(),0)

    def test_collection_current_review_and_hidden_associations(self):
        quiz,q,_=self.make_quiz(self.target)
        other=Topic.objects.create(title='Other subject',slug='other-subject');publish(other,self.editor)
        child=Topic.objects.create(title='Other child',slug='other-child',parent=other);publish(child,self.editor)
        q.related_topics.add(child);review_quiz(quiz,self.editor,'Synthetic source')
        self.assertEqual(self.client.get('/api/topic/other-subject/practice/').json()['count'],1)
        TopicPublication.objects.filter(topic=child).update(is_published=False)
        self.assertEqual(self.client.get('/api/topic/other-subject/practice/').status_code,404)
        self.assertEqual(self.client.get('/api/topic/discovery-target/practice/').status_code,200)

    def test_popup_context_revalidates_current_publication(self):
        response=self.client.get('/api/topic/discovery-target/context/')
        self.assertEqual(response.status_code,200)
        self.assertIn('Published evidence',response.json()['description'])
        TopicPublication.objects.filter(topic=self.target).update(is_published=False)
        self.assertEqual(self.client.get('/api/topic/discovery-target/context/').status_code,404)

    @override_settings(CONNECTION_SCAN_BATCH=1)
    def test_publication_prioritizes_own_scan_and_bounded_queue_can_drain(self):
        self.block.content += '<p>Updated source context.</p>';self.block.save()
        pub=publish(self.source,self.editor)
        self.assertEqual(ConnectionScan.objects.get(publication=pub).source_revision,pub.revision)
        self.assertFalse(ConnectionScan.objects.get(publication=pub).pending)
        for _ in range(10): process_pending(1)
        self.assertFalse(ConnectionScan.objects.filter(pending=True,publication__is_published=True).exists())

    def test_collection_pagination_has_a_bound_manifest_and_no_duplicates(self):
        quiz=Quiz.objects.create(topic=self.source,title='Large reviewed fixture')
        for i in range(51):
            q=Question.objects.create(quiz=quiz,question_text=f'Canonical question {i}',explanation='Synthetic evidence.')
            Choice.objects.create(question=q,choice_text='Evidence',is_correct=True)
            Choice.objects.create(question=q,choice_text='Guess')
        review_quiz(quiz,self.editor,'Synthetic source')
        with CaptureQueriesContext(connection) as queries:
            first=self.client.get('/api/topic/discovery-subject/practice/').json()
        self.assertLessEqual(len(queries),11)
        second=self.client.get('/api/topic/discovery-subject/practice/?page=2').json()
        self.assertEqual(first['count'],51);self.assertEqual(len(first['questions']),50);self.assertEqual(len(second['questions']),1)
        self.assertFalse({q['id'] for q in first['questions']} & {q['id'] for q in second['questions']})
        choice=second['questions'][0]['choices'][0]['id']
        payload={'collection_id':self.root.pk,'page':1,'revision_token':first['revision_token'],'answers':{str(second['questions'][0]['id']):choice}}
        self.assertEqual(self.client.post('/api/topic/discovery-subject/practice/check/',payload,content_type='application/json').status_code,400)
        self.assertEqual(Question.objects.count(),51);self.assertEqual(QuizAttempt.objects.count(),0)


@skipUnless(connection.vendor=='postgresql','Disposable PostgreSQL required for real migration graph')
class DiscoveryMigrationTests(TransactionTestCase):
    def test_reversible_schema_preserves_phase2_records_and_does_not_approve_tags(self):
        before=('content','0007_tag_question_primary_topic_question_related_topics_and_more')
        latest=('content','0008_connectionscan_keywordlinkproposal_tag_is_public_and_more')
        executor=MigrationExecutor(connection);restore=executor.loader.graph.leaf_nodes();executor.migrate([before])
        old=executor.loader.project_state([before]).apps
        try:
            topic=old.get_model('content','Topic').objects.create(title='Legacy',slug='legacy-discovery')
            tag=old.get_model('content','Tag').objects.create(name='Legacy tag',normalized_name='legacy tag',slug='legacy-tag')
            pub=old.get_model('content','TopicPublication').objects.create(topic_id=topic.pk,title='Legacy',is_published=True,snapshot={'slug':topic.slug,'parent_id':None,'blocks':[]})
            pub.tags.add(tag)
            for target in [latest,before,latest]:
                MigrationExecutor(connection).migrate([target])
                self.assertEqual(old.get_model('content','TopicPublication').objects.get(pk=pub.pk).tags.get().pk,tag.pk)
                if target==latest:
                    self.assertFalse(Tag.objects.get(pk=tag.pk).is_public)
                    self.assertTrue(ConnectionScan.objects.get(publication_id=pub.pk).pending)
                    self.assertEqual(KeywordLinkProposal.objects.count(),0)
        finally:
            MigrationExecutor(connection).migrate(restore)


class DiscoverySQLiteMigrationTests(SimpleTestCase):
    def test_forward_reverse_preserves_tag_ids_counters_and_released_associations(self):
        import os, subprocess, sys
        from pathlib import Path
        from tempfile import TemporaryDirectory
        code=r"""
import django
django.setup()
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
before=('content','0007_tag_question_primary_topic_question_related_topics_and_more')
latest=('content','0008_connectionscan_keywordlinkproposal_tag_is_public_and_more')
e=MigrationExecutor(connection);e.migrate([before]);apps=e.loader.project_state([before]).apps
Topic=apps.get_model('content','Topic');Tag=apps.get_model('content','Tag');Publication=apps.get_model('content','TopicPublication')
topic=Topic.objects.create(title='Synthetic source',slug='synthetic-source')
tag=Tag.objects.create(name='Retained tag',normalized_name='retained tag',slug='retained-tag')
pub=Publication.objects.create(topic_id=topic.pk,title=topic.title,is_published=True,snapshot={'slug':topic.slug,'parent_id':None,'blocks':[]})
pub.tags.add(tag)
Tag.objects.create(pk=9002,name='Deleted fixture',normalized_name='deleted',slug='deleted').delete()
for target in [latest,before,latest]:
    MigrationExecutor(connection).migrate([target])
    current=MigrationExecutor(connection).loader.project_state([target]).apps
    assert current.get_model('content','TopicPublication').objects.get(pk=pub.pk).tags.get().pk==tag.pk
    assert current.get_model('content','Tag').objects.get(pk=tag.pk).name=='Retained tag'
    with connection.cursor() as c:
        c.execute('SELECT seq FROM sqlite_sequence WHERE name=%s',['content_tag']);assert c.fetchone()[0]==9002
    if target==latest:
        assert not current.get_model('content','Tag').objects.get(pk=tag.pk).is_public
        assert current.get_model('content','ConnectionScan').objects.get(publication_id=pub.pk).pending
"""
        with TemporaryDirectory(prefix='prepal-phase3-migration-') as directory:
            env={**os.environ,'DJANGO_SETTINGS_MODULE':'core.settings','PYTHON_DOTENV_DISABLED':'1','DATABASE_ENGINE':'sqlite',
                 'DATABASE_PATH':str(Path(directory)/'synthetic.sqlite3'),'DJANGO_ENV':'development','AI_ENABLED':'false',
                 'AI_GUEST_ENABLED':'false','GEMINI_API_KEY':'','GOOGLE_API_KEY':''}
            result=subprocess.run([sys.executable,'-c',code],cwd=Path(__file__).resolve().parents[1],env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr[-2500:])
