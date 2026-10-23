"""Run existing student UI/APIs against an explicitly selected, already prepared local demo."""
import argparse
import json
import os
from pathlib import Path
import signal
import socket
import sqlite3
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def validate_demo():
    if os.environ.get('DJANGO_ENV') == 'production':
        raise ValueError('Student development cannot run in a production environment.')
    selected = os.environ.get('PREPAL_DEMO_ROOT', '')
    if not selected or not Path(selected).is_absolute():
        raise ValueError('Set PREPAL_DEMO_ROOT to an absolute, already prepared student-review directory.')
    root = Path(selected).resolve(strict=True)
    marker = root / '.student-demo.json'
    database = root / 'demo.sqlite3'
    if marker.is_symlink() or not marker.is_file() or database.is_symlink() or not database.is_file():
        raise ValueError('Choose a prepared student review demo; original databases are never opened for writing.')
    record = json.loads(marker.read_text())
    if record.get('kind') != 'prepal-student-review-v2' or record.get('state') != 'ready':
        raise ValueError('Student review preparation is incomplete. Preserve this directory and inspect its logs.')
    with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as connection:
        connection.execute('PRAGMA query_only=ON')
        applied = {row[0] for row in connection.execute("SELECT name FROM django_migrations WHERE app='content'")}
        if '0012_immutable_practice_history' not in applied:
            raise ValueError('Student schema 0012 is required. This launcher never applies migrations.')
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate read-only; do not start servers.')
    parser.add_argument('--backend-only', action='store_true', help='Reuse an existing Vite frontend configured for port 8002.')
    args = parser.parse_args()
    try:
        root = validate_demo()
        if args.check:
            print('Prepared local student environment verified read-only; schema 0012. No migration or server started.')
            return 0
        for port in ((8002,) if args.backend_only else (8002, 5173)):
            with socket.socket() as listener:
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                listener.bind(('127.0.0.1', port))
    except (ValueError, OSError, sqlite3.Error, json.JSONDecodeError):
        # Never print database contents, environment values or credentials in errors.
        parser.error('Select a ready student demo with schema 0012 and free loopback ports 8002/5173. '
                     'Set PREPAL_DEMO_ROOT explicitly; stop older local servers first. No migration is performed.')
    env = {**os.environ, 'PREPAL_DEMO_ROOT': str(root), 'PYTHON_DOTENV_DISABLED': '1',
           'DJANGO_ENV': 'development', 'DJANGO_SETTINGS_MODULE': 'core.student_demo_settings',
           'PREPAL_API_ORIGIN': 'http://127.0.0.1:8002', 'PREPAL_DEV_API_ORIGIN': 'http://127.0.0.1:8002',
           'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': ''}
    commands = [
        [str(ROOT / 'backend/.venv/bin/python'), 'backend/manage.py', 'runserver', '127.0.0.1:8002',
         '--settings=core.student_demo_settings', '--noreload'],
    ]
    if not args.backend_only:
        commands.append(['npm', 'run', 'dev', '--', '--host', '127.0.0.1', '--port', '5173', '--strictPort'])
    children = []

    def stop(_signum, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    try:
        for command in commands:
            children.append(subprocess.Popen(command, cwd=ROOT, env=env, start_new_session=True))
        print('Student development: http://127.0.0.1:5173 — mock AI; Google disabled; production untouched.', flush=True)
        while all(child.poll() is None for child in children):
            time.sleep(.2)
        return next((child.returncode for child in children if child.returncode is not None), 1)
    except KeyboardInterrupt:
        return 0
    finally:
        for child in children:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
        for child in children:
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()


if __name__ == '__main__':
    raise SystemExit(main())
