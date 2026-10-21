"""Prepare the isolated demo only. No real database/environment/provider is used."""
from pathlib import Path
import os
import subprocess
import sys
root = Path(__file__).resolve().parents[1]
demo = Path(os.environ.get('PREPAL_DEMO_ROOT', str(root / '.local/demo'))).resolve()
demo.mkdir(parents=True, exist_ok=True, mode=0o700)
env = {**os.environ, 'PREPAL_DEMO_ROOT': str(demo), 'DJANGO_SETTINGS_MODULE': 'core.demo_settings', 'PYTHON_DOTENV_DISABLED': '1', 'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': '', 'DJANGO_ENV': 'development', 'DEBUG': 'true'}
if (demo / 'demo.sqlite3').exists():
    raise SystemExit('Demo database already exists; preserving it. Use the documented run commands.')
for args in [('migrate', '--noinput'), ('create_demo',)]:
    subprocess.run([sys.executable, 'manage.py', *args], cwd=root / 'backend', env=env, check=True)
