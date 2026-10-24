"""Safe entrypoint: python run_tests.py [test labels / test options]."""
import os
import sys
from pathlib import Path

postgres = '--postgres' in sys.argv
if postgres:
    sys.argv.remove('--postgres')
os.environ["DJANGO_SETTINGS_MODULE"] = "core.postgres_test_settings" if postgres else "core.test_settings"
os.environ["PYTHON_DOTENV_DISABLED"] = "1"

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # Discovery from the repository root must not silently succeed with zero tests.
    os.chdir(Path(__file__).resolve().parent)
    execute_from_command_line([sys.argv[0], "test", *sys.argv[1:]])
