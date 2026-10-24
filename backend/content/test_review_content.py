"""Academic review batches remain isolated and require actual human approval."""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase
from .services.review_content import load_review
from .services.sample_content import load_corpus, note_words
ROOT=Path(__file__).resolve().parents[2]

class ReviewContentTests(SimpleTestCase):
    def test_new_corpus_mapping_lengths_sources_and_questions(self):
        corpus,hierarchy=load_review(); old,_=load_corpus()
        self.assertEqual(len(corpus['lessons']),25)
        self.assertEqual(sum(len(l['questions']) for l in corpus['lessons']),125)
        self.assertTrue(all(400<=note_words(l)<=600 for l in corpus['lessons']))
        self.assertFalse({l['topic_id'] for l in corpus['lessons']} & {l['topic_id'] for l in old['lessons']})
        self.assertEqual(corpus['publication_status'],'draft-human-review-required')
        self.assertTrue(all(s['url'].startswith('https://') for s in corpus['sources'].values()))

    def test_non_demo_seed_is_rejected_before_database_access(self):
        with self.assertRaises(CommandError):call_command('create_review_content')

    def test_new_environment_and_idempotence_preserve_originals_and_require_review(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp)/'new-review'
            env={**os.environ,'PYTHON_DOTENV_DISABLED':'1','PREPAL_DEMO_ROOT':str(root)}
            result=subprocess.run([sys.executable,str(ROOT/'scripts/prepare_student_demo.py'),'--directory',str(root)],cwd=ROOT,env=env,capture_output=True,text=True,timeout=120)
            self.assertEqual(result.returncode,0,result.stderr)
            corpus,_=load_review(); ids=[l['topic_id'] for l in corpus['lessons']]
            db=root/'demo.sqlite3'; before=hashlib.sha256(db.read_bytes()).hexdigest()
            with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True) as conn:
                placeholders=','.join('?' for _ in ids)
                self.assertEqual(conn.execute('select count(*) from content_topic').fetchone()[0],142)
                self.assertEqual(conn.execute('select count(*) from content_question').fetchone()[0],200)
                self.assertEqual(conn.execute('select count(*) from content_choice').fetchone()[0],800)
                self.assertEqual(conn.execute(f'select count(*) from content_topicpublication where is_published=1 and topic_id in ({placeholders})',ids).fetchone()[0],0)
                self.assertEqual(conn.execute(f'select count(*) from content_quizreview r join content_quiz q on r.quiz_id=q.id where q.topic_id in ({placeholders})',ids).fetchone()[0],0)
                self.assertEqual(conn.execute('pragma integrity_check').fetchone()[0],'ok')
                self.assertEqual(conn.execute('pragma foreign_key_check').fetchall(),[])
            again=subprocess.run([sys.executable,str(ROOT/'backend/manage.py'),'create_review_content','--settings=core.student_demo_settings'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(again.returncode,0,again.stderr)
            self.assertEqual(hashlib.sha256(db.read_bytes()).hexdigest(),before)
            rejected=subprocess.run([sys.executable,str(ROOT/'scripts/prepare_student_demo.py'),'--directory',str(root)],cwd=ROOT,env=env,capture_output=True,text=True)
            self.assertNotEqual(rejected.returncode,0)
            inventory=json.loads((root/'review-inventory.json').read_text())
            self.assertFalse(inventory['production_approved']);self.assertEqual(len(inventory['lessons']),25)
