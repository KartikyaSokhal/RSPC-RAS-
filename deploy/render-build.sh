#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pip install --require-hashes -r backend/requirements.txt
npm ci --include=dev
npm run build
PYTHON_DOTENV_DISABLED=1 python backend/manage.py collectstatic --noinput --settings=core.static_build_settings
# Deliberately no migrate, seed, data transfer or credential creation.
