"""Safe preparation, source-corpus contracts and live demo API acceptance."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase

from .services.sample_content import load_corpus, validate_corpus, note_words

ROOT = Path(__file__).resolve().parents[2]


class SampleCorpusTests(SimpleTestCase):
    def test_complete_corpus_uses_original_leaf_topics(self):
        corpus, hierarchy = load_corpus()
        validate_corpus(corpus, hierarchy)
        self.assertEqual(sum(len(row['questions']) for row in corpus['lessons']), 75)
        self.assertTrue(all(400 <= note_words(row) <= 600 for row in corpus['lessons']))

    def test_invalid_question_or_syllabus_classification_is_rejected(self):
        corpus, hierarchy = load_corpus()
        cases = [lambda c: c['lessons'][0].update(topic_id=5),
                 lambda c: c['lessons'][0]['questions'][0].update(answer=True),
                 lambda c: c['lessons'][0]['questions'][0].update(choices=['Duplicate'] * 4),
                 lambda c: c['lessons'][0]['connections'][0].update(target_id=30)]
        for mutate in cases:
            with self.subTest(mutate=mutate):
                invalid = copy.deepcopy(corpus)
                mutate(invalid)
                with self.assertRaises(CommandError):
                    validate_corpus(invalid, hierarchy)

    def test_seed_refuses_non_demo_settings_before_accessing_database(self):
        with self.assertRaisesMessage(CommandError, 'outside a new marked isolated demo'):
            call_command('create_sample_content')

    def test_existing_destination_and_symlink_are_preserved(self):
        with TemporaryDirectory() as temporary:
            existing = Path(temporary) / 'valuable'
            existing.mkdir()
            sentinel = existing / 'demo.sqlite3'
            sentinel.write_bytes(b'valuable existing data')
            alias = Path(temporary) / 'alias'
            alias.symlink_to(existing, target_is_directory=True)
            for destination in (existing, alias):
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/prepare_sample_demo.py'),
                                         '--directory', str(destination)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('preserving it', result.stderr)
                self.assertEqual(sentinel.read_bytes(), b'valuable existing data')

    def test_fresh_demo_and_read_only_api_verification_then_repeat_refusal(self):
        with TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'sample'
            env = {**os.environ, 'PREPAL_DEMO_ROOT': str(destination), 'PYTHON_DOTENV_DISABLED': '1'}
            def run(*args):
                return subprocess.run([sys.executable, *args], cwd=ROOT, env=env,
                                      capture_output=True, text=True, timeout=120)
            prepared = run('scripts/prepare_sample_demo.py', '--directory', str(destination))
            self.assertEqual(prepared.returncode, 0, prepared.stderr)
            database = destination / 'demo.sqlite3'
            before = hashlib.sha256(database.read_bytes()).hexdigest()
            verified = run('scripts/verify_sample_demo.py')
            self.assertEqual(verified.returncode, 0, verified.stderr)
            report = json.loads(verified.stdout)
            self.assertEqual(report['Question'], 75)
            self.assertEqual(report['approved_links'], 30)
            self.assertEqual(report['Bookmark'] + report['QuizAttempt'] + report['UserProgress'], 0)
            self.assertGreater(report['http_requests_verified'], 90)
            repeat = run('scripts/prepare_sample_demo.py', '--directory', str(destination))
            self.assertNotEqual(repeat.returncode, 0)
            seeded_again = run('backend/manage.py', 'create_sample_content', '--settings=core.demo_settings')
            self.assertNotEqual(seeded_again.returncode, 0)
            self.assertIn('preserving it', seeded_again.stderr)
            self.assertEqual(hashlib.sha256(database.read_bytes()).hexdigest(), before)
