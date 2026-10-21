# Phase A remediation — production remains undeployed

The owner approved the local baseline commit after verification. Local development key rotation is complete; no production secret/connection changed. The known key remains historical but is inactive locally and blocked by the current production insecure-prefix guard. Never reuse it or any demo/test secret for production; provision independent credentials through the future approved environment. External reuse is unverified.

Read-only SSH confirmed remote codex/prepal-1-0 at ee272a6954868b303447545eb553200adb024a24 and main at e6e7989db8c24eee59f8c38600cd619939c96856 before the local commit; main contains the retired key. No push/history rewrite occurred. Phase B requires separate approval, then remote SHA and CI checks; gh CLI authentication is currently absent. No staging/production URL, hosting/domain or real PostgreSQL source/target is selected. Phases C–F remain pending, including PDF export/Tutor isolation, durable recovery, timeout alignment and staging acceptance. Procedures below are gated future operations.

---

# Current release gate after controlled cleanup

Release preparation uses an explicit manifest of current worktree inputs, including untracked services, migrations and canonical docs. A hash-verified disposable export has no original databases, private environment, demo credentials, old environments or retired Node backend. Installation and local tests are distinct from publication: the working branch/HEAD remain unchanged and nothing is committed/pushed.

Production blockers remain: approved destination/roles/TLS/CA, domain and CSRF hosts, trusted proxy configuration, durable database-plus-media backup/restore, human corpus/rights approval and real-host load/permission/security validation. Set STATIC_ROOT and PRIVATE_MEDIA_ROOT to match the proxy/systemd paths; the defaults are not those example directories. PDF preparation is synchronous with a 60-second parser limit while proxy/worker examples permit 40/45 seconds; resolve its execution/timeout policy separately before production Admin use. Keep AI disabled until model compatibility, pricing/caps and live evaluation are explicitly approved. Uploaded PDF viewing/download is implemented; topic-note PDF export is not.

CI now includes release/document checks and a separately prepared academic sample/browser suite. Remote CI is unverified until an approved publication/run. Do not provision or cut over during cleanup. The procedures below describe future approved operations, not commands automatically executed by this batch.

---

Current schema target is content 0008 (34 tables); verified only on disposable loopback PostgreSQL/SQLite. Real cutover remains separately gated. Account for queued `regenerate_connections` batches in an approved future operational schedule; no scheduler/paid service is provisioned here. Do not run commands against the original SQLite archive. Back up proposal decisions/plans and public-tag metadata before any approved rollback.

Historical Phase 2 schema target was content migration 0007, verified on disposable local databases only. Real cutover remains pending explicit approval; do not apply this migration to the original SQLite archive. Update the reviewed deployment migration/backup inventory for the 32-table schema when a real target is approved. Local Docker/tmpfs verification is not durable hosting or backup provisioning.

# Phase 1 setup, cutover gate and recovery

No production host/domain/credentials or real cutover is configured by Phase 1. Nginx/systemd/Gunicorn files remain reviewable examples. PostgreSQL is now the required default database; SQLite is an untouched source archive and explicit isolated demo/test option.

## Local PostgreSQL

Install PostgreSQL 17 locally or run the official PostgreSQL image on a loopback-only port. Phase 1 found no local server binaries and started the installed Docker Desktop for a disposable container. The verified server was PostgreSQL 17.11; exact image digest and artifacts are in evidence (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`). Do not reuse rehearsal credentials or a temporary database for production.

Create private credentials outside Git and a new empty local development database. Supply `DATABASE_ENGINE=postgresql`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST=127.0.0.1`, `POSTGRES_PORT` and an appropriate local `POSTGRES_SSLMODE`. The [example](../backend/.env.example) contains no password. Do not display environment files or connection URLs in logs. Normal settings fail clearly if required PostgreSQL variables are missing; there is no automatic SQLite fallback.

Install the hash-pinned backend dependencies. Only after confirming that the selected DB is a new disposable development database, run `backend/.venv/bin/python backend/manage.py migrate --noinput`. This command is not authorized for the real source/production DB by Phase 1. Then start the normal Django server and Vite as documented in [README](../README.md). Do not seed the original database or reuse the SQLite-only demo generator against PostgreSQL.

## Verification commands

Fast SQLite: `backend/.venv/bin/python backend/run_tests.py`. PostgreSQL: set `PREPAL_TEST_POSTGRES=1`, an existing empty `prepal_test_*` base DB and `POSTGRES_TEST_DB=test_prepal_phase1`, then run `backend/.venv/bin/python backend/run_tests.py --postgres`. PostgreSQL tests genuinely execute migrations, refuse any already-existing test database, and destroy only the fresh DB created by the test runner. See [testing](TESTING.md).

`backend/.venv/bin/python scripts/verify_postgres_transfer.py` builds a new synthetic SQLite fixture and exercises migration/transfer with explicit local PostgreSQL settings. For the source-data rehearsal command, use [DATABASE_SCHEMA](DATABASE_SCHEMA.md). These tools refuse remote destinations and never implement cutover. Browser integration additionally requires an explicit absolute PREPAL_DEMO_ROOT and refuses the existing .local/demo path.

## Native PostgreSQL backup and restore

Use a matching PostgreSQL client version, a new private destination and a coherent media backup. Freeze editorial/file-processing writes while pairing database and media snapshots. `pg_dump` is a consistent DB snapshot but cannot independently freeze external media. Native clients use PG* environment variables, while Django configuration uses POSTGRES_*.

Prepared commands, to be executed only for an approved source/destination:

```sh
umask 077
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump --host "$POSTGRES_HOST" --port "$POSTGRES_PORT" \
  --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --format=custom \
  --no-owner --no-privileges --file "$PREPAL_NEW_DUMP_FILE"
# Create a separately approved NEW EMPTY restore database; never overwrite an existing one.
PGPASSWORD="$POSTGRES_PASSWORD" pg_restore --host "$POSTGRES_HOST" --port "$POSTGRES_PORT" \
  --username "$POSTGRES_USER" --dbname "$PREPAL_NEW_RESTORE_DB" --exit-on-error \
  --no-owner --no-privileges "$PREPAL_NEW_DUMP_FILE"
```

Set native TLS/CA variables consistently with the approved environment; do not put passwords in CLI arguments/URLs. Phase 1 used Docker's matching native tools inside the isolated container. A fresh restored local target was checked with `scripts/verify_postgres_restore.py`, preserving all 26 tables and 24 sequence states. The SQLite-only `backup_prepal` helper now refuses PostgreSQL explicitly instead of treating a database name as a SQLite filename.

For that verification helper set `POSTGRES_DB` to the restored local `prepal_rehearsal_*` DB, `PREPAL_REHEARSAL_COPY` to the private `migrated/migration-copy.sqlite3`, and `PRIVATE_MEDIA_ROOT` to the restored private media directory. The helper selects isolated rehearsal settings and performs read-only record/sequence checks.

## Real cutover — owner review required

Before approval, select the production host/database, TLS/CA, runtime/migration roles, secret environment, private media path and durable encrypted/off-host backup destination/retention. Production requires `DJANGO_ENV=production`, DEBUG=false, a strong SECRET_KEY, explicit hosts/CSRF origins, PostgreSQL password and `POSTGRES_SSLMODE=verify-full`. Runtime credentials should not have CREATEDB or superuser permissions. Rehearsal's local superuser role and disabled TLS are not production settings.

Proposed cutover after separate approval:

1. Freeze source/editorial writes and verify a fresh private source+media backup and restore. Reconfirm current Git/config/source inventory; do not reuse an old temporary snapshot as fresh evidence.
2. Repeat the validated local copy migration/transfer from that frozen source. Review hashes, IDs, constraints, sequence counters and real content eligibility.
3. Back up the verified PostgreSQL copy natively and restore it into a separately approved new empty production target; preserve source migration metadata and verify target schema/data/media. No fake migrations or data truncation.
4. Review the production environment/roles/TLS and switch database configuration only after explicit approval. Check pending migration plan, administrative CSRF/login, publication/search, approved PDF/image serving, stateless practice and learner denial. Keep AI default-off.
5. Verify the real reverse proxy, private media denial, CSP/PDF workers, process limits, load, monitoring and durable restore procedures on the actual host. Public exposure/deployment requires its own approval.

Rollback: stop writes/exposure, preserve any post-cutover writes, and restore the last verified PostgreSQL+media backup to a new database before an approved configuration switch. If new writes occurred, reconcile them rather than discard them. Retain the original SQLite archive and protected code snapshot for re-rehearsal. Current code must not automatically fall back to the unmigrated original SQLite file. No source replacement, real migration, credential edit, deployment, commit or push was performed in Phase 1.
