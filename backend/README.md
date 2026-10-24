# Prepal Django backend

Python 3.14.6, Django 6/DRF, PostgreSQL via hash-pinned psycopg and Django Admin. Install `requirements-dev.txt` with `--require-hashes` in backend/.venv as described in the [root README](../README.md). Retired Express/Mongo code remains private and is not a launch path.

## Configuration

Normal settings require explicit PostgreSQL variables from [.env.example](.env.example). Set a fresh private SECRET_KEY; never reuse the retired development key. Production requires HTTPS, explicit hosts/CSRF origins, PostgreSQL verify-full TLS, least-privilege runtime role and protected persistent media. [Deployment](../docs/DEPLOYMENT.md) lists approval gates.

Source schema ends at content **0012**. Migrations 0001–0008 are unchanged. New migrations cover identity/rate windows, explicit reading visits, deterministic plans and immutable attempt snapshots. Original SQLite remains 0004; existing demos stay at their recorded versions. No real cutover or original migration has occurred. Only newly created review/test databases use the new schema.

`STUDENT_FEATURES_ENABLED` defaults false in both normal development and production. The safe template explicitly sets false. Enable it only on an approved current schema. Closed-gate APIs return a constant 503 before auth/body processing; enabled handlers require session ownership/CSRF. Ownerless legacy rows remain unassigned and inaccessible.

## Google and recovery email

Configure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET and GOOGLE_REDIRECT_URI privately. Register the exact callback `/api/auth/google/callback/` on the same backend origin, e.g. `http://127.0.0.1:5173/api/auth/google/callback/` through Vite's same-origin proxy. Use the same host throughout; localhost and 127.0.0.1 cookies are distinct. Use HTTPS on production. Start is a CSRF-protected POST; callback validates state/nonce/PKCE, signed audience/issuer/expiry and verified email. Duplicate email does not automatically link Google to password/staff accounts. Tests mock token exchange; no bypass endpoint exists.

Set SITE_ORIGIN to the student-facing origin (HTTPS in production). Configure EMAIL_HOST/PORT/USER/PASSWORD, EMAIL_USE_TLS and DEFAULT_FROM_EMAIL. Password reset uses a 30-minute single-use Django token in a URL fragment, not access logs; the page clears the fragment after reading it. SMTP failures return the same generic request result for account privacy. Delivery and live Google consent still require authorized external validation. Password registrations do not currently perform email verification; decide the production policy before opening registration.

## Development and checks

Use the [new student review demo](../README.md#isolated-student-review-demo) for local accounts/plans. `core.student_demo_settings` requires an explicitly selected marked isolated root, uses an in-memory mailbox, clears Google/provider secrets and enables only mock Tutor. Existing `core.demo_settings` keeps learner features disabled.

```sh
backend/.venv/bin/python backend/run_tests.py
backend/.venv/bin/python backend/manage.py check --settings=core.test_settings
backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
```

The default runner uses isolated SQLite and mocked providers. Guarded PostgreSQL tests use real migrations and refuse nonlocal or existing test databases; see [TESTING](../docs/TESTING.md). Never point tests at application data.

Admin retains notes/preview/review/publish/withdraw, approved PDFs and canonical question review. New topic study estimates are approximate total learning/revision/practice minutes. The 25 new academic lessons and quizzes remain drafts pending human review. See [workflow](../docs/ADMIN_WORKFLOW.md), [schema](../docs/DATABASE_SCHEMA.md) and [API](../docs/API_DOCUMENTATION.md).

## Lock maintenance

Only under separately authorized dependency maintenance:

```sh
cd backend
uv pip compile requirements.in --python .venv/bin/python --generate-hashes -o requirements.txt
uv pip compile requirements-dev.in --python .venv/bin/python --generate-hashes -o requirements-dev.txt
```

The driver supplies no database server. Gunicorn/proxy examples are not deployed services. PDF extraction can take 60 seconds, exceeding current proxy/worker examples (40/45); production timeout alignment remains required.

## Restore local student navigation

Use `PREPAL_DEMO_ROOT=/absolute/prepared/student-review npm run dev:student -- --check` at the application root. The launcher requires a ready marker/schema0012 and does not migrate. Cold start uses npm run dev:student (backend8002/frontend5173); when Vite is already running use --backend-only and ignored .env.local with PREPAL_DEV_API_ORIGIN=http://127.0.0.1:8002. See the root README. An older core.demo_settings server remains content-only, regardless of frontend navigation.

The local frontend must report student_features_enabled=true through /api/config/ before showing accounts. Google availability remains false in student-demo settings. Do not set a frontend learner flag or change production environment values to work around a closed backend.

## Isolated PostgreSQL student candidate (no cutover)

Supply a NEW private setup environment outside the checkout, mode0600: DATABASE_ENGINE=postgresql, DJANGO_ENV=development, POSTGRES_DB=postgres, POSTGRES_HOST=127.0.0.1, POSTGRES_PORT, POSTGRES_USER/PASSWORD and POSTGRES_SSLMODE for the local setup administrator, plus PREPAL_LOCAL_POSTGRES_SETUP=1. Use a secure editor/password manager; do not echo credentials or commit the file. Provision only on an approved local PostgreSQL service. Native clients must match/support the server (current drill16.2; production17 unverified). The temporary test cluster is not a persistent supported installation.

From the application root, using absolute private paths:

```sh
backend/.venv/bin/python scripts/postgres_ops.py provision-local \
  --env-file "$PREPAL_PRIVATE_ADMIN_ENV" --database prepal_local_student_dev \
  --new-directory "$PREPAL_NEW_CREDENTIALS_DIRECTORY"
# This creates a NEW database; migrate it only with migration.env.
backend/.venv/bin/python scripts/postgres_ops.py run-env \
  --env-file "$PREPAL_NEW_CREDENTIALS_DIRECTORY/migration.env" -- \
  backend/.venv/bin/python backend/manage.py migrate --noinput --settings=core.local_postgres_settings
backend/.venv/bin/python scripts/postgres_ops.py run-env \
  --env-file "$PREPAL_NEW_CREDENTIALS_DIRECTORY/runtime.env" -- \
  backend/.venv/bin/python backend/manage.py check --settings=core.local_postgres_settings
```

Provision refuses existing databases/directories, remote hosts and names outside prepal_local_/prepal_rehearsal_. It generates three independent role passwords and a fresh candidate signing key, saved only to private env files. Migration owner has no cluster-admin rights; runtime has CRUD, sequence USAGE/SELECT and ten connections; backup SELECT/two connections; no runtime DDL/sequence reset or backup writes. Migration role has two connections. Runtime default connection age0; connect5s, statement15s, lock5s, idle-transaction60s; bounded POSTGRES_* overrides are in backend/.env.example. Migration file uses a120s statement limit. Do not use migration credentials for the application.

Learners default off. Only after separate local target acceptance, set STUDENT_FEATURES_ENABLED=true in that private runtime candidate file and explicitly select core.local_postgres_settings. Do not switch the8002 source or development proxy until cutover approval. Set private MEDIA_ROOT/ALLOWED_HOSTS/site configuration explicitly; CLI uses PYTHON_DOTENV_DISABLED=1. Guarded staging/production profiles require DJANGO_ENV=production and matching PREPAL_ENVIRONMENT and force learners/AI/Google off. They are unactivated. Backup/restore commands and policy gates are in [deployment](../docs/DEPLOYMENT.md).

## Render staging candidate

From the repository root, `bash deploy/render-build.sh` installs locked dependencies/builds React/collects static files without migrations or real DB access. `bash deploy/render-start.sh` selects guarded core.render_settings with HTTPS, staging access credentials and an external persistent private-media path. The process refuses incomplete configuration. Follow [deployment](../docs/DEPLOYMENT.md); do not use production credentials for local tests or relax PostgreSQL verify-full.
