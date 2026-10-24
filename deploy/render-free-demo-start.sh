#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../backend"
export PYTHON_DOTENV_DISABLED=1
export DJANGO_SETTINGS_MODULE=core.free_demo_settings
exec python -m gunicorn core.wsgi:application --config ../deploy/render-gunicorn.conf.py
# No migrations, content seeding or fallback to SQLite.
