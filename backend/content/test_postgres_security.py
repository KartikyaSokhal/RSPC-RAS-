"""Security/configuration and non-destructive account-deletion approval gate."""
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, TestCase, Client, override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.database import database_config
from .models import Bookmark, Topic, UserProgress
from .services.postgres_ops import local_target, load_environment, write_private
from .services.postgres_backup import media_inventory, record_status, status, retention_candidates


class PostgresConfigurationTests(SimpleTestCase):
    def env(self):
        return {'POSTGRES_DB': 'prepal_local_test', 'POSTGRES_USER': 'runtime', 'POSTGRES_HOST': '127.0.0.1'}

    def test_bounded_timeouts_and_connections(self):
        config = database_config(self.env())
        self.assertEqual(config['CONN_MAX_AGE'], 0)
        self.assertIn('statement_timeout=15000', config['OPTIONS']['options'])
        for key, value in [('POSTGRES_CONNECT_TIMEOUT', '0'), ('POSTGRES_CONN_MAX_AGE', '301'),
                           ('POSTGRES_STATEMENT_TIMEOUT_MS', '1000 -c log_statement=all'),
                           ('POSTGRES_LOCK_TIMEOUT_MS', '-1'), ('POSTGRES_IDLE_TRANSACTION_TIMEOUT_MS', '9999999')]:
            with self.assertRaises(ImproperlyConfigured): database_config(self.env() | {key: value})

    def test_production_tls_and_no_sqlite_fallback(self):
        for extra in ({}, {'POSTGRES_PASSWORD': 'synthetic', 'POSTGRES_SSLMODE': 'require'}):
            with self.assertRaises(ImproperlyConfigured): database_config(self.env() | extra, production=True)
        self.assertEqual(database_config(self.env() | {'POSTGRES_PASSWORD': 'synthetic'}, production=True)['OPTIONS']['sslmode'], 'verify-full')
        with self.assertRaises(ImproperlyConfigured): database_config({'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': ':memory:'}, production=True)

    def test_local_tools_refuse_remote_and_valuable_targets(self):
        for host, name in [('example.invalid', 'prepal_local_test'), ('127.0.0.1', 'production'), ('127.0.0.1', 'prepal_local_a;DROP')]:
            with self.assertRaises(ValueError): local_target({'POSTGRES_HOST': host}, name)

    def test_private_files_media_and_backup_health(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary); env = root / 'private.env'
            write_private(env, 'POSTGRES_DB=prepal_local_test\n')
            self.assertEqual(load_environment(env)['POSTGRES_DB'], 'prepal_local_test')
            env.chmod(0o644)
            with self.assertRaises(ValueError): load_environment(env)
            self.assertFalse(status(root)['healthy']); record_status(root, True); self.assertTrue(status(root)['healthy'])
            record_status(root, False); self.assertFalse(status(root)['healthy'])
            self.assertEqual(retention_candidates(root, 30), [])
            (root / 'link').symlink_to(env)
            with self.assertRaises(ValueError): media_inventory(root)

    def test_explicit_profiles_remain_closed_or_refuse_wrong_environment(self):
        backend = Path(__file__).resolve().parents[1]
        base = {**os.environ, **self.env(), 'POSTGRES_PASSWORD': 'synthetic', 'POSTGRES_SSLMODE': 'verify-full',
                'PYTHON_DOTENV_DISABLED': '1', 'SECRET_KEY': 'synthetic-configuration-only-never-used-as-a-real-key-123456789',
                'DJANGO_ENV': 'production', 'DEBUG': 'false', 'ALLOWED_HOSTS': '127.0.0.1', 'STUDENT_FEATURES_ENABLED': 'true'}
        for profile in ('staging', 'production'):
            result = subprocess.run([sys.executable, '-c', f'from core.{profile}_settings import STUDENT_FEATURES_ENABLED, AI_ENABLED; print(STUDENT_FEATURES_ENABLED, AI_ENABLED)'],
                                    cwd=backend, env=base | {'PREPAL_ENVIRONMENT': profile}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0); self.assertEqual(result.stdout.strip(), 'False False')
        result = subprocess.run([sys.executable, '-c', 'import core.local_postgres_settings'], cwd=backend, env=base, capture_output=True)
        self.assertNotEqual(result.returncode, 0)


@override_settings(STUDENT_FEATURES_ENABLED=True)
class DeletionSecurityTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('deletion-student', email='deletion@example.invalid', password='Long-pass-for-tests-475!')
        self.other = User.objects.create_user('other-student', password='Other-pass-for-tests-475!')
        self.topic = Topic.objects.create(title='Shared syllabus', slug='deletion-shared')
        Bookmark.objects.create(user=self.user, topic=self.topic)
        UserProgress.objects.create(user=self.user, topic=self.topic, is_completed=True)
        self.client.force_login(self.user)

    def counts(self):
        return [model.objects.count() for model in (get_user_model(), Bookmark, UserProgress, Topic)]

    def test_authenticated_readiness_is_scoped_and_never_deletes(self):
        before = self.counts()
        response = self.client.get('/api/account/deletion/')
        self.assertEqual(response.status_code, 200); self.assertFalse(response.json()['deletion_enabled'])
        self.assertEqual(response.json()['records']['bookmarks'], 1)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get('/api/account/deletion/').json()['records']['bookmarks'], 0)
        self.assertEqual(self.counts(), before)

    def test_confirmation_reauth_and_approval_gate(self):
        before = self.counts()
        for data, expected in [({'password': 'wrong', 'confirmation': 'DELETE MY ACCOUNT'}, 403),
                               ({'password': 'Long-pass-for-tests-475!', 'confirmation': 'yes'}, 400),
                               ({'password': 'Long-pass-for-tests-475!', 'confirmation': 'DELETE MY ACCOUNT', 'user_id': self.other.pk}, 400),
                               ({'password': 'Long-pass-for-tests-475!', 'confirmation': 'DELETE MY ACCOUNT'}, 409)]:
            self.assertEqual(self.client.post('/api/account/deletion/', data, content_type='application/json').status_code, expected)
        self.assertEqual(self.counts(), before)
        self.assertEqual(self.client.delete('/api/account/deletion/').status_code, 405)

    def test_csrf_guest_and_closed_gate(self):
        self.assertEqual(Client().get('/api/account/deletion/').status_code, 401)
        browser = Client(enforce_csrf_checks=True); browser.force_login(self.user)
        self.assertEqual(browser.post('/api/account/deletion/', {}, content_type='application/json').status_code, 403)
        with override_settings(STUDENT_FEATURES_ENABLED=False):
            for method in ('get', 'post', 'delete'):
                response = getattr(Client(), method)('/api/account/deletion/')
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.json()['error']['code'], 'learner_features_unavailable')

    def test_password_reset_invalidates_other_persisted_session_and_token(self):
        browser = Client(); browser.force_login(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk)); token = default_token_generator.make_token(self.user)
        response = self.client.post('/api/auth/password-reset/confirm/', {'uid': uid, 'token': token, 'password': 'Changed-long-password-482!'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(browser.get('/api/auth/status/').json()['authenticated'])
        self.assertEqual(self.client.post('/api/auth/password-reset/confirm/', {'uid': uid, 'token': token, 'password': 'Another-long-password-482!'}, content_type='application/json').status_code, 400)
        self.user.refresh_from_db(); self.assertTrue(self.user.check_password('Changed-long-password-482!'))


class EncryptedRecoveryTests(SimpleTestCase):
    """Native local crypto only; no database/network/provider is used."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        import shutil
        from unittest import SkipTest
        cls.openssl = shutil.which('openssl')
        if not cls.openssl or not subprocess.run([cls.openssl, 'version'], capture_output=True).stdout.startswith((b'OpenSSL 3.', b'OpenSSL 4.')):
            raise SkipTest('OpenSSL 3+ CMS AES-GCM is required for encrypted recovery tests.')
        cls.temporary = TemporaryDirectory(); cls.root = Path(cls.temporary.name)
        from .services.postgres_backup import run
        run([cls.openssl, 'req', '-x509', '-newkey', 'rsa:2048', '-noenc', '-days', '1', '-subj', '/CN=Synthetic recovery tests',
             '-keyout', str(cls.root / 'recipient-private.pem'), '-out', str(cls.root / 'recipient.crt')])
        (cls.root / 'recipient-private.pem').chmod(0o600)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'temporary'): cls.temporary.cleanup()
        super().tearDownClass()

    def encrypted(self, name, *, cipher='-aes-256-gcm', unsafe=False):
        import io
        import tarfile
        from .services.postgres_backup import run, digest
        source = self.root / (name + '-source'); source.mkdir(mode=0o700)
        (source / 'database.dump').write_bytes(b'Synthetic native dump placeholder')
        (source / 'media').mkdir(); (source / 'media/note.txt').write_text('Synthetic media')
        (source / 'manifest.json').write_text(json.dumps({'format': 1, 'dump_sha256': digest(source / 'database.dump'), 'media': {'note.txt': digest(source / 'media/note.txt')}}))
        with tarfile.open(source / 'bundle.tar', 'w') as archive:
            for item in ('database.dump', 'manifest.json', 'media'): archive.add(source / item, arcname=item)
            if unsafe:
                item = tarfile.TarInfo('../outside'); item.size = 1; archive.addfile(item, io.BytesIO(b'x'))
        bundle = self.root / (name + '.cms')
        run([self.openssl, 'cms', '-encrypt', '-binary', cipher, '-outform', 'DER', '-in', str(source / 'bundle.tar'), '-out', str(bundle), str(self.root / 'recipient.crt')])
        bundle.chmod(0o600); return bundle

    def test_authenticated_roundtrip_and_existing_destination_refusal(self):
        from .services.postgres_backup import extract
        bundle = self.encrypted('roundtrip'); target = self.root / 'roundtrip-restore'
        result = extract(bundle, self.root / 'recipient-private.pem', target, self.openssl)
        self.assertEqual(result['format'], 1)
        self.assertEqual((target / 'media/note.txt').read_text(), 'Synthetic media')
        with self.assertRaises(FileExistsError): extract(bundle, self.root / 'recipient-private.pem', target, self.openssl)

    def test_tamper_and_truncation_are_rejected_before_extraction(self):
        from .services.postgres_backup import extract
        bundle = self.encrypted('damaged')
        for kind in ('tamper', 'truncate'):
            data = bytearray(bundle.read_bytes())
            if kind == 'tamper': data[len(data)//2] ^= 1
            else: data = data[:len(data)//2]
            bad = self.root / (kind + '.cms'); bad.write_bytes(data); bad.chmod(0o600)
            target = self.root / (kind + '-restore')
            with self.assertRaises(ValueError): extract(bad, self.root / 'recipient-private.pem', target, self.openssl)
            self.assertFalse(target.exists())

    def test_non_aead_cipher_is_rejected(self):
        from .services.postgres_backup import extract
        bundle = self.encrypted('cbc', cipher='-aes-256-cbc')
        with self.assertRaises(ValueError): extract(bundle, self.root / 'recipient-private.pem', self.root / 'cbc-restore', self.openssl)

    def test_path_traversal_is_rejected(self):
        from .services.postgres_backup import extract
        bundle = self.encrypted('unsafe', unsafe=True)
        with self.assertRaises(ValueError): extract(bundle, self.root / 'recipient-private.pem', self.root / 'unsafe-restore', self.openssl)
        self.assertFalse((self.root / 'outside').exists())
