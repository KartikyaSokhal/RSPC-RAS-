"""Forward/reverse learner migrations only on explicitly disposable PostgreSQL."""
from unittest import skipUnless
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase

@skipUnless(connection.vendor=='postgresql','Requires disposable PostgreSQL --postgres')
class StudentMigrationTests(TransactionTestCase):
    def test_forward_reverse_preserves_legacy_owned_and_ownerless_records(self):
        old=[('content','0008_connectionscan_keywordlinkproposal_tag_is_public_and_more')]
        new=[('content','0012_immutable_practice_history')]
        executor=MigrationExecutor(connection)
        try:
            executor.migrate(old); apps=executor.loader.project_state(old).apps
            User=apps.get_model('auth','User'); Topic=apps.get_model('content','Topic')
            user=User.objects.create(username='migration-fixture-user',password='!')
            topic=Topic.objects.create(title='Legacy syllabus fixture',slug='migration-fixture')
            quiz=apps.get_model('content','Quiz').objects.create(topic=topic,title='Legacy fixture')
            for owner in (None,user.pk):
                apps.get_model('content','Bookmark').objects.create(topic=topic,user_id=owner)
                apps.get_model('content','UserProgress').objects.create(topic=topic,user_id=owner,is_completed=True)
                apps.get_model('content','QuizAttempt').objects.create(quiz=quiz,user_id=owner,score=1,total_questions=2)
            models=['Bookmark','UserProgress','QuizAttempt']
            before={name:list(apps.get_model('content',name).objects.order_by('pk').values()) for name in models}
            executor=MigrationExecutor(connection);executor.migrate(new); modern=executor.loader.project_state(new).apps
            self.assertEqual(modern.get_model('content','StudentIdentity').objects.count(),0)
            self.assertEqual(modern.get_model('content','StudyPlan').objects.count(),0)
            for name,rows in before.items():
                after=list(modern.get_model('content',name).objects.order_by('pk').values())
                self.assertEqual([{k:r[k] for k in rows[0]} for r in after],rows)
            executor=MigrationExecutor(connection);executor.migrate(old); legacy=executor.loader.project_state(old).apps
            for name,rows in before.items():self.assertEqual(list(legacy.get_model('content',name).objects.order_by('pk').values()),rows)
        finally:
            MigrationExecutor(connection).migrate(new)
