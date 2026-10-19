"""Safe entrypoint: python run_tests.py [test labels / test options]."""
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "core.test_settings"
os.environ["PYTHON_DOTENV_DISABLED"] = "1"

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line([sys.argv[0], "test", *sys.argv[1:]])
