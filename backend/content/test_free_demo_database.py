"""No hosted credentials, database or provider used by these guard regressions."""
from pathlib import Path
from tempfile import TemporaryDirectory
from django.test import SimpleTestCase
from unittest.mock import patch
from content.services.free_demo_database import target,HOST,DATABASE,corpus_digest,prepare
from content.services.postgres_ops import load_environment,write_private


class FreeDemoDatabaseGuards(SimpleTestCase):
    def env(self):
        return dict(DATABASE_ENGINE='postgresql',POSTGRES_HOST=HOST,POSTGRES_DB=DATABASE,
                    POSTGRES_SSLMODE='verify-full',PREPAL_FREE_DEMO='1',PREPAL_FREE_DEMO_SYNTHETIC_DATA='1')

    def test_exact_render_identity_and_confirmations(self):
        target(self.env())
        for changes in ({'POSTGRES_HOST':HOST.split('.')[0]},{'POSTGRES_DB':'production'},
                        {'POSTGRES_SSLMODE':'require'},{'PREPAL_FREE_DEMO':'0'},
                        {'PREPAL_FREE_DEMO_SYNTHETIC_DATA':''},{'DATABASE_ENGINE':'sqlite'}):
            with self.assertRaises(ValueError):target(self.env()|changes)

    def test_local_exception_cannot_select_hosted_or_existing_app_database(self):
        for host,name in ((HOST,DATABASE),('127.0.0.1','production'),('localhost','prepal_free_demo_test_new')):
            with self.assertRaises(ValueError):target(self.env()|{'POSTGRES_HOST':host,'POSTGRES_DB':name},True)
        target(self.env()|{'POSTGRES_HOST':'127.0.0.1','POSTGRES_DB':'prepal_free_demo_test_new'},True)

    def test_private_configuration_is_mandatory(self):
        with TemporaryDirectory() as root:
            p=Path(root)/'private.env';write_private(p,'POSTGRES_DB=synthetic\n')
            self.assertEqual(load_environment(p)['POSTGRES_DB'],'synthetic')
            p.chmod(0o644)
            with self.assertRaises(ValueError):load_environment(p)
            link=Path(root)/'link';link.symlink_to(p)
            with self.assertRaises(ValueError):load_environment(link)

    def test_corpus_identity_is_stable(self):
        self.assertEqual(corpus_digest(),corpus_digest());self.assertEqual(len(corpus_digest()),64)

    def test_credentials_cannot_be_generated_inside_release_source(self):
        with TemporaryDirectory() as root:
            config=Path(root)/'private.env'
            write_private(config,'\n'.join(k+'='+v for k,v in self.env().items()))
            output=Path(__file__).resolve().parents[2]/'should-never-contain-secrets'
            with patch('content.services.free_demo_database.connect') as connection:
                with self.assertRaises(ValueError):prepare(config,output)
                connection.assert_not_called()
