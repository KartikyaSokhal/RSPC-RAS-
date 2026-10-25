#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../backend"
export PYTHON_DOTENV_DISABLED=1
export DJANGO_SETTINGS_MODULE=core.render_public_demo_settings
# Read-only identity, corpus, synthetic-account and runtime-permission gate.
python manage.py check_public_demo
exec python -m gunicorn core.wsgi:application --config ../deploy/render-gunicorn.conf.py
# Never migrate, create accounts, grant privileges or seed at startup.
