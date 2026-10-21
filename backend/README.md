# Prepal Django backend

Use Python 3.14.6, Django 6/DRF, PostgreSQL (psycopg 3) and Django Admin. Active environment: `backend/.venv`. Retired Express/Mongo code and the obsolete environment are archived privately and must not be restored into startup/deployment paths.

## Install and test

From the application root, create backend/.venv and install `backend/requirements-dev.txt` with pip's `--require-hashes` option as shown in [README](../README.md). Runtime/dev locks and their .in sources are unchanged. Run `backend/run_tests.py` with the backend interpreter; its default is isolated in-memory SQLite and mocked AI, never the original database. `manage.py check --settings=core.test_settings` and `makemigrations --check --dry-run --settings=core.test_settings` are non-applying checks. No migrations are authorized during documentation cleanup.

Normal settings require explicit PostgreSQL variables from the [template](.env.example); no implicit SQLite fallback is allowed. Production requires separate approved secrets/hosts/TLS/roles/media/backups. See [schema](../docs/DATABASE_SCHEMA.md), [deployment](../docs/DEPLOYMENT.md) and [security](../docs/SECURITY.md). Current target is content 0008; the original archive remains 0004 and is never an application runtime path.

The exposed local development key was rotated previously; backend/.env remains ignored, mode 0600 and unchanged by this cleanup. Never restore the retired value or add a fallback. Old local sessions/reset links/cookies/practice tokens require reauthentication/reload; passwords/content remain stored. Production secrets must be independently generated under separate approval. No credential changes are authorized here.

## Existing demos and editorial workflow

Use [existing academic demo startup](../README.md#academic-sample-demo--21-october-2026). core.demo_settings selects explicit SQLite/mock AI and never loads real environment credentials. The sample tooling seeds only new private empty destinations; do not run preparation/migrations in this cleanup or reset existing demos. `verify_sample_demo.py` is query-only and detects manual corpus drift. Its 15 lessons/75 questions and engineering review flags are not production editorial/rights approval.

Topic-tree/WYSIWYG authoring, private previews, review, publish/withdraw, controlled tags/aliases/relations and reviewed canonical question associations remain in Django Admin. Learner endpoints/reports stay closed while administrative staff login works. See [workflow](../docs/ADMIN_WORKFLOW.md) and [HTTP API](../docs/API_DOCUMENTATION.md).

Gunicorn binds privately behind a TLS proxy. Align STATIC_ROOT/PRIVATE_MEDIA_ROOT with approved host paths. PDF extraction's 60-second bound exceeds the current proxy/worker examples (40/45 seconds); resolve under future production scope before use. No live server, cutover or deployment is verified by local tests.

## Lock maintenance

For separately authorized dependency maintenance, from backend:

```sh
uv pip compile requirements.in --python .venv/bin/python --generate-hashes -o requirements.txt
uv pip compile requirements-dev.in --python .venv/bin/python --generate-hashes -o requirements-dev.txt
```

The psycopg binary wheel supplies the client driver, not a PostgreSQL server. PostgreSQL tests require an explicitly isolated local disposable target; see [verification](../docs/TESTING.md). Existing migrations/models/locks and data are preserved.
