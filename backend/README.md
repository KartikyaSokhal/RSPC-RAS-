# Current backend setup after controlled cleanup

Local development SECRET_KEY was rotated after historical exposure; it stays only in ignored backend/.env with mode 0600. Do not restore the retired value from history/private backups or add a fallback. Reauthenticate/reload practice after rotation; passwords/content remain unchanged. Configure an independently generated production key only under the approved production environment procedure. See [security](../docs/SECURITY.md) and [current handoff](../docs/AGENT_HANDOFF.md).

Use Python 3.14.6 and `backend/.venv`. The old `backend/env` and retired `backend/package.json`, `backend/package-lock.json`, `backend/src` are privately archived and absent from release inputs. Do not restore them into startup paths. Hash-locked `requirements*.txt` and their `.in` sources remain unchanged.

From the application root, create a fresh environment and install `backend/requirements-dev.txt` with `--require-hashes` as shown in README. Run `backend/run_tests.py`, `manage.py check --settings=core.test_settings` and `manage.py makemigrations --check --dry-run --settings=core.test_settings`. These checks must not use the original database. SQLite demo preparation applies existing schema only to a new disposable directory.

Current schema target is content 0008; original SQLite remains an immutable 0004 archive. Gunicorn's private listener is intended for PostgreSQL runtime. Production setup must explicitly align static/private-media paths with the proxy/service configuration. Synchronous PDF preparation can exceed the example proxy/worker timeouts; resolve/test that separately before production. No real cutover is performed by cleanup.

---

# Academic sample demo

Use the application-root commands in [README](../README.md#academic-sample-demo--21-october-2026). `scripts/prepare_sample_demo.py` exclusively creates a new destination, applies the existing schema and calls `create_sample_content` under `core.demo_settings`. The command validates the corpus, requires an explicit preparation marker and an empty topic/user/tag database, then inserts the original hierarchy and sample records transactionally. It uses existing publish, review_quiz, suggestion/decision and collection services; no models, routes, migrations or provider implementations changed.

`content/fixtures/sample_lessons_v1.json` is the versioned content source; `content/services/sample_content.py` validates it and verifies resulting publications, questions, tags, links and pools. `scripts/verify_sample_demo.py` enforces SQLite query-only mode and tests API/CSRF/stateless behavior with provider/network construction blocked. New regression coverage is `content/test_sample_content.py`; browser coverage uses a separate `npm run test:sample` suite. The earlier synthetic `create_demo` corpus remains unchanged for existing tests.

---

# Phase 3 discovery

New migration 0008 adds evidence-bound phrase proposals, queued scans/derived link plans and explicit public-tag approval. It is verified only on disposable databases; original SQLite remains untouched. Public reading performs no phrase analysis or writes. Admin publication/suggestion/review updates plans; `regenerate_connections --limit 20` drains queued work. New routes provide current context, approved tags and canonical stateless practice. Read [Admin workflow](../docs/ADMIN_WORKFLOW.md), [API](../docs/API_DOCUMENTATION.md) and [current verification](../docs/TESTING.md). The Phase 2 foundation below is retained; its discovery deferrals are superseded.

# Phase 2 content foundation

Migration 0007 adds the controlled registry, associations and editorial state. It is verified only on disposable databases; never migrate the original SQLite archive. Admin primary sections are Topics, Content and Practice Questions. Topic snapshots remain the notes publication unit; a Question remains one canonical record. See [current verification](../docs/TESTING.md) and [handoff](../docs/AGENT_HANDOFF.md).

# Prepal Django backend

Primary backend: Django 6/DRF, PostgreSQL (psycopg 3) and Django Admin. Historical Express/Mongo launch commands are unsupported. Student features are unavailable in this content-first release; Django administrative authentication remains functional.

Private PostgreSQL environment and source-preserving migration procedure: [database](../docs/DATABASE_SCHEMA.md), [deployment/recovery](../docs/DEPLOYMENT.md). The real SQLite archive is not a runtime fallback. Production credentials, migrations/cutover and deployment require separate approval.

Synthetic demo: `core.demo_settings` selects SQLite/mock AI, with optional `PREPAL_DEMO_ROOT` for a new private directory. `scripts/prepare_demo.py` refuses an existing database. It never seeds PostgreSQL or valuable application data.

Tests from either application root or backend: use `backend/run_tests.py` (or `.venv/bin/python run_tests.py` inside backend). Default is SQLite :memory:, no .env or migrations. `--postgres` selects explicitly opted-in local disposable PostgreSQL settings and actual migrations. See [test isolation/results](../docs/TESTING.md).

Dependency regeneration from backend, preserving reviewed version pins:

```sh
uv pip compile requirements.in --python .venv/bin/python --generate-hashes -o requirements.txt
uv pip compile requirements-dev.in --python .venv/bin/python --generate-hashes -o requirements-dev.txt
```

Install with `pip install --require-hashes -r requirements-dev.txt`. No PostgreSQL server is installed automatically by these dependencies; the binary wheel supplies the Python driver/libpq client. See [Admin workflow](../docs/ADMIN_WORKFLOW.md) and Phase 1 evidence (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).
