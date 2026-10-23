"""Local student startup and fail-closed configuration; never opens original data for writing."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('prepal_student_dev', ROOT / 'scripts/run_student_dev.py')
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class StudentEnvironmentTests(SimpleTestCase):
    def test_normal_development_and_production_require_explicit_student_opt_in(self):
        for mode, flag, expected in [('development', None, 'False'), ('development', 'true', 'True'),
                                     ('production', None, 'False'), ('production', 'false', 'False')]:
            env = {**os.environ, 'PYTHON_DOTENV_DISABLED': '1', 'DJANGO_ENV': mode, 'DEBUG': 'false',
                   'ALLOWED_HOSTS': '127.0.0.1', 'SECRET_KEY': secrets.token_urlsafe(48),
                   'DATABASE_ENGINE': 'postgresql', 'POSTGRES_DB': 'prepal_test_config',
                   'POSTGRES_USER': 'synthetic', 'POSTGRES_HOST': '127.0.0.1',
                   'POSTGRES_PASSWORD': 'synthetic-unused', 'POSTGRES_SSLMODE': 'verify-full'}
            env.pop('STUDENT_FEATURES_ENABLED', None)
            if flag is not None: env['STUDENT_FEATURES_ENABLED'] = flag
            command = [sys.executable, '-c', 'from core.settings import STUDENT_FEATURES_ENABLED; print(STUDENT_FEATURES_ENABLED)']
            result = subprocess.run(command, cwd=ROOT / 'backend', env=env, capture_output=True, text=True, check=True)
            self.assertEqual(result.stdout.strip(), expected)

    def fixture(self, root, *, ready=True, migrated=True):
        (root / '.student-demo.json').write_text(json.dumps({'kind': 'prepal-student-review-v2', 'state': 'ready' if ready else 'preparing'}))
        with sqlite3.connect(root / 'demo.sqlite3') as database:
            database.execute('CREATE TABLE django_migrations (app TEXT, name TEXT)')
            if migrated: database.execute("INSERT INTO django_migrations VALUES ('content', '0012_immutable_practice_history')")

    def test_check_mode_accepts_ready_review_without_migration_or_database_writes(self):
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve(); self.fixture(root)
            before = hashlib.sha256((root / 'demo.sqlite3').read_bytes()).hexdigest()
            env = {**os.environ, 'PREPAL_DEMO_ROOT': str(root), 'DJANGO_ENV': 'development'}
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/run_student_dev.py'), '--check'], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn('verified read-only', result.stdout)
            self.assertEqual(hashlib.sha256((root / 'demo.sqlite3').read_bytes()).hexdigest(), before)

    def test_missing_explicit_path_and_production_are_rejected(self):
        for env in ({'DJANGO_ENV': 'development'}, {'PREPAL_DEMO_ROOT': str(ROOT / '.local/demo'), 'DJANGO_ENV': 'production'}):
            with patch.dict(os.environ, env, clear=True), self.assertRaises(ValueError): launcher.validate_demo()

    def test_legacy_unmarked_demo_is_rejected_without_creating_database(self):
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with patch.dict(os.environ, {'PREPAL_DEMO_ROOT': str(root), 'DJANGO_ENV': 'development'}), self.assertRaises(ValueError):
                launcher.validate_demo()
            self.assertFalse((root / 'demo.sqlite3').exists())

    def test_incomplete_and_unmigrated_demos_are_preserved_and_refused(self):
        for ready, migrated in [(False, True), (True, False)]:
            with TemporaryDirectory() as directory:
                root = Path(directory).resolve(); self.fixture(root, ready=ready, migrated=migrated)
                before = (root / 'demo.sqlite3').read_bytes()
                with patch.dict(os.environ, {'PREPAL_DEMO_ROOT': str(root), 'DJANGO_ENV': 'development'}), self.assertRaises(ValueError):
                    launcher.validate_demo()
                self.assertEqual((root / 'demo.sqlite3').read_bytes(), before)

    def test_database_symlink_is_rejected_before_reading_target(self):
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve(); self.fixture(root)
            target = root / 'preserved.sqlite3'; (root / 'demo.sqlite3').rename(target)
            (root / 'demo.sqlite3').symlink_to(target)
            with patch.dict(os.environ, {'PREPAL_DEMO_ROOT': str(root), 'DJANGO_ENV': 'development'}), self.assertRaises(ValueError):
                launcher.validate_demo()
