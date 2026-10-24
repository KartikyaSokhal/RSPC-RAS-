from pathlib import Path
import sqlite3
import tempfile
from django.test import SimpleTestCase
from .services.backups import backup, restore, inventory


class BackupTests(SimpleTestCase):
    def test_complete_copy_preserves_rows_files_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source.sqlite3'
            with sqlite3.connect(source) as con:
                con.execute('CREATE TABLE notes (id INTEGER PRIMARY KEY, text TEXT)')
                con.execute("INSERT INTO notes VALUES (9, 'Synthetic fixture')")
            media = root / 'media'; media.mkdir(); (media / 'fixture.txt').write_text('fixture')
            backup(source, media, root / 'backup')
            result = restore(root / 'backup', root / 'restored')
            self.assertEqual(result, {'tables_verified': 1, 'media_verified': 1})
            self.assertEqual(inventory(source), inventory(root / 'restored/database.sqlite3'))
            with self.assertRaises(FileExistsError):
                restore(root / 'backup', root / 'restored')
            (root / 'backup/database.sqlite3').write_bytes(b'corrupted fixture')
            with self.assertRaises(ValueError):
                restore(root / 'backup', root / 'another')
