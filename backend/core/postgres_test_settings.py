"""PostgreSQL tests are opt-in and restricted to named disposable local databases."""
from .test_settings import *  # noqa: F403
from .database import database_config
from django.core.exceptions import ImproperlyConfigured

if os.environ.get('PREPAL_TEST_POSTGRES') != '1':
    raise ImproperlyConfigured('PostgreSQL tests require PREPAL_TEST_POSTGRES=1.')
config = database_config({**os.environ, 'DATABASE_ENGINE': 'postgresql'})
test_name = os.environ.get('POSTGRES_TEST_DB', 'test_prepal_phase1')
if (config['HOST'] not in ('127.0.0.1', 'localhost', '::1')
        or not config['NAME'].startswith('prepal_test_') or not test_name.startswith('test_prepal_')):
    raise ImproperlyConfigured('Tests require loopback, prepal_test_* base and test_prepal_* test databases.')
config['TEST'] = {'NAME': test_name}
DATABASES = {'default': config}
TEST_RUNNER = 'core.test_runner.PostgresRunner'
