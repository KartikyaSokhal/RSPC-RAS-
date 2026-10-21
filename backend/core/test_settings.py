"""P000 tests never load .env or open the application database."""
import os
from unittest.mock import patch

with patch("dotenv.load_dotenv"), patch.dict(os.environ, {
    'DATABASE_ENGINE': 'sqlite', 'DATABASE_PATH': ':memory:',
    'DJANGO_ENV': 'development', 'AI_ENABLED': 'false', 'AI_GUEST_ENABLED': 'false',
    'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': '',
}):
    from .settings import *  # noqa: F403

SECRET_KEY = "test-only-not-a-production-secret-000000000000000000000000"
DEBUG = False
ALLOWED_HOSTS = ["testserver"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
TEST_RUNNER = "core.test_runner.NoMigrationRunner"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
os.environ["GEMINI_API_KEY"] = ""
os.environ["GOOGLE_API_KEY"] = ""
os.environ["PYTHON_DOTENV_DISABLED"] = "1"

# Never inherit real editorial approvals into synthetic test fixtures.
APPROVED_QUIZ_IDS = ()
