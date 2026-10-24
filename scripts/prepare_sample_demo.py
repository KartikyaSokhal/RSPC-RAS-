"""Create a NEW local sample database; never open an existing destination."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MARKER = 'prepal-academic-sample-v1'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True,
                        help='New private directory; existing directories are refused.')
    args = parser.parse_args()
    destination = args.directory.expanduser().resolve()
    if destination.exists():
        parser.error('Destination already exists; preserving it. Choose a new directory.')
    # mkdir is exclusive, including across simultaneous invocations. Never reset.
    destination.mkdir(mode=0o700, parents=True, exist_ok=False)
    marker = destination / '.sample-demo.json'
    marker.write_text(json.dumps({'kind': MARKER, 'state': 'preparing'}))
    marker.chmod(0o600)
    env = {**os.environ, 'PREPAL_DEMO_ROOT': str(destination),
           'DJANGO_SETTINGS_MODULE': 'core.demo_settings', 'PYTHON_DOTENV_DISABLED': '1',
           'GEMINI_API_KEY': '', 'GOOGLE_API_KEY': '', 'DJANGO_ENV': 'development'}
    for command in [('migrate', '--noinput'), ('create_sample_content',)]:
        subprocess.run([sys.executable, 'manage.py', *command], cwd=ROOT / 'backend',
                       env=env, check=True)
    print(f'Sample demo ready: {destination} (mock AI only).')


if __name__ == '__main__':
    main()
