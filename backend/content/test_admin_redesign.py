from tempfile import TemporaryDirectory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Topic, ContentBlock, TopicPublication, TopicRelation, Quiz, Question, Choice, Bookmark, UserProgress, QuizAttempt, LearningResource, QuizReview
from .services.publication import publish, sanitize
from .services.quiz import review_quiz


class AdminRedesignTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(username='admin-super', password='super-password-123', email='super@prepal.local')
        self.staff_editor = User.objects.create_user(username='staff-editor', password='staff-password-123', email='editor@prepal.local', is_staff=True)
        self.student = User.objects.create_user(username='learner-priya', password='student-pass-123', email='priya@student.local')

        # Create ContentTypes and assign complete editorial staff permissions
        for model_name, app_name in [('topic', 'content'), ('contentblock', 'content'), ('learningresource', 'content'), ('quiz', 'content'), ('question', 'content'), ('choice', 'content'), ('user', 'auth')]:
            ct, _ = ContentType.objects.get_or_create(app_label=app_name, model=model_name)
            for action in ['add', 'change', 'view']:
                p, _ = Permission.objects.get_or_create(content_type=ct, codename=f'{action}_{model_name}', defaults={'name': f'Can {action} {model_name}'})
                self.staff_editor.user_permissions.add(p)

        self.root_topic = Topic.objects.create(title='Ancient Rajasthan History', slug='ancient-rajasthan', order=1)
        self.child_topic = Topic.objects.create(title='Palaeolithic Sites of Rajasthan', slug='palaeolithic-sites', parent=self.root_topic, order=2)
        self.related_topic = Topic.objects.create(title='Mesolithic Bagor & Tilwara', slug='mesolithic-bagor', parent=self.root_topic, order=3)

        self.block1 = ContentBlock.objects.create(
            topic=self.child_topic,
            block_type='text',
            content='<h2>Early Human Settlements</h2><p>Archaeological evidence discovered along Luni river basin.</p>',
            source_reference='Archaeological Survey of India',
            order=1
        )

        publish(self.root_topic, self.superuser)
        publish(self.child_topic, self.superuser)
        publish(self.related_topic, self.superuser)

    def test_staff_editor_sees_content_sections_without_learner_reports(self):
        self.client.force_login(self.staff_editor)
        res = self.client.get('/admin/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()

        # Three primary sections exist
        self.assertIn('Topics', content)
        self.assertIn('Practice Questions', content)
        self.assertNotIn('3. Students', content)

        # Technical models are hidden from ordinary staff editors
        self.assertIn('Content blocks', content)
        self.assertNotIn('Resource pages', content)
        self.assertNotIn('Quiz reviews', content)
        self.assertIn('Learning resources', content)
        self.assertNotIn('Advanced Technical Models', content)

    def test_superuser_sees_advanced_technical_section(self):
        self.client.force_login(self.superuser)
        res = self.client.get('/admin/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()

        self.assertIn('Topics', content)
        self.assertIn('Practice Questions', content)
        self.assertNotIn('3. Students', content)
        self.assertIn('Users', content)
        self.assertIn('Advanced maintenance (Superuser)', content)
        self.assertIn('Content blocks', content)

    def test_syllabus_tree_view_renders_hierarchical_structure(self):
        self.client.force_login(self.staff_editor)
        tree_url = reverse('admin:content_topic_tree')
        res = self.client.get(tree_url)
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()

        self.assertIn('Syllabus Hierarchy Explorer', content)
        self.assertIn('Ancient Rajasthan History', content)
        self.assertIn('Palaeolithic Sites of Rajasthan', content)
        self.assertIn('Published v1', content)
        self.assertIn('Edit Notes', content)
        self.assertIn('Preview', content)

    def test_topic_single_workflow_actions(self):
        self.client.force_login(self.superuser)
        change_url = reverse('admin:content_topic_change', args=[self.child_topic.pk])

        # 1. Edit draft notes
        self.block1.content = '<h2>Updated Evidence</h2><p>Excavations confirm micro-blade industries.</p>'
        self.block1.save()

        # 2. Publish live via single-click workflow
        res_pub = self.client.post(change_url, {'_publish_now': '1'}, follow=True)
        self.assertEqual(res_pub.status_code, 200)
        self.child_topic.refresh_from_db()
        pub = TopicPublication.objects.get(topic=self.child_topic)
        self.assertTrue(pub.is_published)
        self.assertEqual(pub.revision, 2)
        self.assertIn('Updated Evidence', pub.snapshot['blocks'][0]['content'])

        # 3. Withdraw via workflow
        res_with = self.client.post(change_url, {'_withdraw_now': '1'}, follow=True)
        self.assertEqual(res_with.status_code, 200)
        pub.refresh_from_db()
        self.assertFalse(pub.is_published)

        # 4. Restore previous snapshot via workflow
        res_rest = self.client.post(change_url, {'_restore_previous': '1'}, follow=True)
        self.assertEqual(res_rest.status_code, 200)
        pub.refresh_from_db()
        self.assertTrue(pub.is_published)
        self.assertGreater(pub.revision, 2)

    def test_quiz_authoring_and_approval_workflow_hides_unapproved_from_students(self):
        quiz = Quiz.objects.create(topic=self.child_topic, title='Prehistory MCQ Test', time_limit_seconds=300)
        q1 = Question.objects.create(
            quiz=quiz,
            question_text='Which river valley yielded key Lower Palaeolithic tools in Rajasthan?',
            explanation='The Luni and its tributaries like Gambhiri yielded prominent handaxes.'
        )
        c1 = Choice.objects.create(question=q1, choice_text='Luni River Basin', is_correct=True)
        c2 = Choice.objects.create(question=q1, choice_text='Ganga Basin', is_correct=False)
        c3 = Choice.objects.create(question=q1, choice_text='Narmada Basin', is_correct=False)
        c4 = Choice.objects.create(question=q1, choice_text='Yamuna Basin', is_correct=False)

        # Unapproved quiz is hidden from students
        client = APIClient()
        self.assertEqual(client.get(f'/api/topic/{self.child_topic.slug}/quiz/').status_code, 404)

        # Approve quiz via QuizAdmin change form
        self.client.force_login(self.superuser)
        quiz_change_url = reverse('admin:content_quiz_change', args=[quiz.pk])
        res = self.client.post(quiz_change_url, {'_approve_quiz': '1'}, follow=True)
        self.assertEqual(res.status_code, 200)

        # Now quiz is approved and student can access it
        self.assertTrue(QuizReview.objects.filter(quiz=quiz, is_approved=True).exists())
        student_res = client.get(f'/api/topic/{self.child_topic.slug}/quiz/')
        self.assertEqual(student_res.status_code, 200)
        self.assertEqual(student_res.json()['title'], 'Prehistory MCQ Test')

        # Editing a choice invalidates approval fingerprint automatically
        c2.choice_text = 'Altered Wrong Choice'
        c2.save()
        # Immediately hidden from students again
        self.assertEqual(client.get(f'/api/topic/{self.child_topic.slug}/quiz/').status_code, 404)

    def test_student_progress_report_view(self):
        UserProgress.objects.create(user=self.student, topic=self.child_topic, is_completed=True)
        Bookmark.objects.create(user=self.student, topic=self.root_topic)

        quiz = Quiz.objects.create(topic=self.child_topic, title='Prehistory Practice')
        q1 = Question.objects.create(quiz=quiz, question_text='Where is Bagor?', explanation='In Bhilwara.')
        Choice.objects.create(question=q1, choice_text='Bhilwara', is_correct=True)
        Choice.objects.create(question=q1, choice_text='Jaipur', is_correct=False)
        review_quiz(quiz, self.superuser, 'Archaeological Survey')

        QuizAttempt.objects.create(user=self.student, quiz=quiz, score=1, total_questions=1)

        # Phase 1 supersedes the earlier learner-report release decision.
        for actor in (self.superuser, self.staff_editor, self.student):
            self.client.force_login(actor)
            report_url = reverse('admin:content_student_report', args=[self.student.pk])
            self.assertIn(self.client.get(report_url).status_code, (302, 403))
        self.assertEqual(QuizAttempt.objects.filter(user=self.student).count(), 1)
        self.assertEqual(UserProgress.objects.filter(user=self.student).count(), 1)
        self.assertEqual(Bookmark.objects.filter(user=self.student).count(), 1)

    def test_accidental_deletion_safeguards(self):
        from .admin import TopicAdmin, StudentUserAdmin
        from django.contrib.admin.sites import AdminSite

        site = AdminSite()
        topic_admin = TopicAdmin(Topic, site)
        student_admin = StudentUserAdmin(get_user_model(), site)

        # Neither topics nor students can be deleted through admin
        self.assertFalse(topic_admin.has_delete_permission(None))
        self.assertFalse(student_admin.has_delete_permission(None))

    def test_topic_relation_association(self):
        rel = TopicRelation.objects.create(
            source=self.child_topic,
            target=self.related_topic,
            kind='related',
            reason='Chronological continuation from Palaeolithic to Mesolithic'
        )
        self.assertEqual(rel.source, self.child_topic)
        self.assertEqual(rel.target, self.related_topic)

    def test_wysiwyg_html_sanitization_preserves_tables_headings_and_cleans_script(self):
        dirty = (
            '<h2>Major Excavation</h2>'
            '<table class="educational-table"><thead><tr><th>Site</th><th>Period</th></tr></thead>'
            '<tbody><tr><td>Didwana</td><td>Lower Palaeolithic</td></tr></tbody></table>'
            '<blockquote class="exam-note">📌 Key Point: Oldest tools found here.</blockquote>'
            '<script>alert("hacked")</script>'
            '<iframe src="https://evil.com"></iframe>'
            '<img src="https://evil.com/x.jpg" onerror="alert(1)">'
        )
        cleaned = sanitize(dirty)
        self.assertIn('<h2>Major Excavation</h2>', cleaned)
        self.assertIn('<table', cleaned)
        self.assertIn('<th>Site</th>', cleaned)
        self.assertIn('<td>Didwana</td>', cleaned)
        self.assertIn('<blockquote>📌 Key Point', cleaned)
        self.assertNotIn('<script', cleaned)
        self.assertNotIn('<iframe', cleaned)
        self.assertNotIn('<img', cleaned)
        self.assertNotIn('onerror', cleaned)

    def test_pdf_preparation_cannot_automatically_approve_or_republish(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        from django.contrib import admin
        from django.core.files.base import ContentFile
        from django.test import RequestFactory
        from .admin import ResourceAdmin, TopicAdmin
        request = RequestFactory().post('/admin/')
        request.user = self.superuser
        resource = LearningResource(topic=self.child_topic, title='Synthetic PDF', source_reference='Synthetic', rights_note='Original fixture')
        resource.file.save('fixture.pdf', ContentFile(b'%PDF-synthetic'), save=False)
        revision = TopicPublication.objects.get(topic=self.child_topic).revision
        def prepared(pk):
            LearningResource.objects.filter(pk=pk).update(status='ready')
        with patch('content.services.resources.process_resource', side_effect=prepared), patch('content.services.resources.approve_resource') as approve:
            ResourceAdmin(LearningResource, admin.site).save_model(request, resource, None, False)
            resource.refresh_from_db()
            self.assertEqual(resource.status, 'ready')
            approve.assert_not_called()
        resource.status = 'pending'
        resource.save()
        with patch('django.contrib.admin.ModelAdmin.save_related'), patch('content.admin.process_resource', side_effect=prepared), patch('content.admin.approve_resource') as approve:
            TopicAdmin(Topic, admin.site).save_related(request, SimpleNamespace(instance=self.child_topic), [], True)
            resource.refresh_from_db()
            self.assertEqual(resource.status, 'ready')
            approve.assert_not_called()
        self.assertEqual(TopicPublication.objects.get(topic=self.child_topic).revision, revision)
