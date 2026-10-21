# Deployment and recovery gates

No staging or production environment, URL, domain/provider, production credential or real database cutover is established. Current work is an uncommitted documentation/ignore cleanup over 49407b2; no commit/push/merge/history rewrite/deployment is authorized. The last audit found old GitHub main still contains a retired development key. Do not deploy that tree or assume a future normal commit erases history. See [security](SECURITY.md).

## Ordered approvals

1. Owner reviews cleanup diff/security evidence, then separately authorizes any local commit.
2. Separate push approval; verify exact approved local SHA, live remote refs, ordinary branch push and matching remote SHA/CI. Never force-push/amend/rewrite history. SSH reads worked at audit; gh CLI was unauthenticated.
3. Complete master Phase C: published-snapshot topic-note PDF export and server-enforced current-topic Tutor, with security/mock/regression proof. Paid model credentials/budget remain a separate gate.
4. Owner selects production source data, PostgreSQL target/roles/TLS, durable encrypted off-host backup destination/retention and approves fresh backup/restore/rehearsal/rollback before any real transfer/configuration switch.
5. Owner approves hosting/provider/domain/access and any billing. Prepare staging before separate final production acceptance/approval. Do not assume demo data or old learner records belong in production.

## Existing host examples and prerequisites

Review deploy/nginx.conf.example, deploy/prepal-proxy.conf.example, deploy/prepal.service.example and backend/gunicorn.conf.py on the actual approved host. They are examples, not verified infrastructure. Django's listener is private loopback, behind a TLS reverse proxy. Set DJANGO_ENV=production, DEBUG=false, a fresh strong SECRET_KEY, explicit ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS, PostgreSQL credentials and POSTGRES_SSLMODE=verify-full with trusted CA. Runtime role must not be superuser/CREATEDB; separate approved migration role and bounded connection settings are required.

Vite builds the SPA for same-origin /api. Serve only dist/static assets with SPA fallback and suitable hashed-asset caching; never serve repository/private-media/.env/.git paths. Collect Django static files only in approved deployment scope. Align STATIC_ROOT and PRIVATE_MEDIA_ROOT with service/proxy locations; defaults differ from the examples. Private media requires persistent protected storage and reviewed application delivery, not a public directory alias.

Configure HTTPS, trusted proxy overwrite rules, secure cookies/CSRF/CSP/HSTS, upload/rate limits, controlled Admin access and health/monitoring/restart procedures. Logs omit query strings/request bodies/credentials. Validate real filesystem ownership, persistence, process limits and recovery independently of the developer Mac. No key belongs in VITE_* or a source file.

PDF processing may run 60 seconds while proxy/Gunicorn examples allow 40/45. Resolve and test execution/timeouts under approved production scope; runtime configuration is unchanged here. Uploaded-PDF reading is implemented; topic-note PDF export is not. Keep live AI off until approved model/non-thinking compatibility, pricing/caps/billing and factual/citation evaluation.

## Database and rehearsal

Source migrations 0001–0008 remain unchanged. Original SQLite is content 0004 and immutable; existing demos are preserved. Prior PostgreSQL schema/ID/foreign-key/sequence/publication transfer and migration reversal/restore proofs used disposable targets only. [DATABASE_SCHEMA](DATABASE_SCHEMA.md) holds rehearsal/configuration details. Never fake migrations or run cutover tools against a valuable original database. No migration application or new demo preparation is authorized during this documentation cleanup.

Future approved PostgreSQL tests must use explicitly named disposable loopback databases and the guarded --postgres runner; production credentials are forbidden. Local tmpfs/Docker success is not durable production backup.

## Backup, restore and rollback

Before approved cutover, freeze editorial/file writes and pair a coherent source/database/media backup. pg_dump snapshots do not freeze external media. Use matching native PostgreSQL clients, private environment credentials and a NEW private dump destination; native clients read PG* variables while Django uses POSTGRES_*.

Prepared future commands, NOT executed in this cleanup:

```sh
umask 077
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump --host "$POSTGRES_HOST" --port "$POSTGRES_PORT" \
  --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --format=custom \
  --no-owner --no-privileges --file "$PREPAL_NEW_DUMP_FILE"
# Independently approved NEW EMPTY restore target; never overwrite an existing database.
PGPASSWORD="$POSTGRES_PASSWORD" pg_restore --host "$POSTGRES_HOST" --port "$POSTGRES_PORT" \
  --username "$POSTGRES_USER" --dbname "$PREPAL_NEW_RESTORE_DB" --exit-on-error \
  --no-owner --no-privileges "$PREPAL_NEW_DUMP_FILE"
```

Supply consistent native TLS/CA variables privately; do not print environment values or password URLs. Independently restore/compare tables, rows, constraints, PKs, migration metadata, sequence high-water marks, publication decisions and paired media before switching connections. Keep durable encrypted backups outside application storage with approved retention and monitoring; private temporary snapshots are not that service.

Rollback stops writes/exposure, preserves any post-cutover changes and restores the approved DB/media backup to a NEW target before a separately approved configuration switch. Reconcile new writes rather than discarding them. Retain original SQLite, private archives and rollback assets for approved retention. No automatic fallback to the original archive. [TESTING](TESTING.md) separates local evidence from unverified staging/production requirements.
