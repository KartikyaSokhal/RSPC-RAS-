"""Configuration and transfer safety checks; never connects to an external DB."""
import datetime
from types import SimpleNamespace
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, Resolver404
from core.database import database_config
from .services.database_transfer import assert_disposable_target, canonical


class DatabaseSafetyTests(SimpleTestCase):
    def test_default_requires_postgres_configuration_without_sqlite_fallback(self):
        with self.assertRaises(ImproperlyConfigured):
            database_config({})
        config = database_config({'POSTGRES_DB': 'prepal_test', 'POSTGRES_USER': 'fixture', 'POSTGRES_HOST': '127.0.0.1'})
        self.assertEqual(config['ENGINE'], 'django.db.backends.postgresql')
        self.assertNotIn('DATABASE_PATH', config)
        with self.assertRaises(ImproperlyConfigured):
            database_config({'DATABASE_ENGINE': 'unknown'})

    def test_sqlite_requires_explicit_path_and_is_refused_in_production(self):
        from pathlib import Path
        original = str(Path(__file__).resolve().parents[1] / 'db.sqlite3')
        for env, production in [({'DATABASE_ENGINE': 'sqlite'}, False),
                                ({'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': ':memory:'}, True),
                                ({'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': original}, False)]:
            with self.assertRaises(ImproperlyConfigured):
                database_config(env, production=production)
        self.assertEqual(database_config({'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': ':memory:'})['NAME'], ':memory:')

    def test_postgres_production_requires_password_and_verified_tls(self):
        env = {'POSTGRES_DB': 'synthetic', 'POSTGRES_USER': 'synthetic', 'POSTGRES_HOST': 'db.invalid'}
        with self.assertRaises(ImproperlyConfigured):
            database_config(env, production=True)
        for mode in ('disable', 'prefer', 'require', 'invalid'):
            with self.assertRaises(ImproperlyConfigured):
                database_config({**env, 'POSTGRES_PASSWORD': 'synthetic-unused', 'POSTGRES_SSLMODE': mode}, production=True)
        config = database_config({**env, 'POSTGRES_PASSWORD': 'synthetic-unused'}, production=True)
        self.assertEqual(config['OPTIONS']['sslmode'], 'verify-full')
        for port in ('0', '65536', 'invalid'):
            with self.assertRaises(ImproperlyConfigured):
                database_config({**env, 'POSTGRES_PORT': port})

    def test_transfer_refuses_other_engines_remote_hosts_and_nonrehearsal_names(self):
        for vendor, name, host in [('sqlite', 'prepal_rehearsal_test', '127.0.0.1'),
                                   ('postgresql', 'prepal', '127.0.0.1'),
                                   ('postgresql', 'prepal_rehearsal_test', 'db.invalid')]:
            with self.assertRaises(ValueError):
                assert_disposable_target(SimpleNamespace(vendor=vendor, settings_dict={'NAME': name, 'HOST': host}))

    def test_transfer_canonicalization_compares_equivalent_timestamps(self):
        utc = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
        local = utc.astimezone(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        self.assertEqual(canonical(utc), canonical(local))

    def test_raw_private_media_has_no_public_url_route(self):
        for path in ('/private-media/draft.pdf', '/private-media/resources/secret.pdf', '/media/draft.pdf'):
            with self.assertRaises(Resolver404):
                resolve(path)


class AttachmentReviewTests(TestCase):
    def test_legacy_raw_attachment_is_retained_but_cannot_bypass_resource_review(self):
        from .models import Topic, ContentBlock
        from .services.publication import publish
        topic = Topic.objects.create(title='Synthetic lesson', slug='attachment-review')
        block = ContentBlock.objects.create(topic=topic, block_type='pdf', file='content/legacy.pdf', order=1)
        publish(topic, None)
        response = self.client.get('/api/topic/attachment-review/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['blocks'][0]['file'])
        block.refresh_from_db()
        self.assertEqual(block.file.name, 'content/legacy.pdf')
