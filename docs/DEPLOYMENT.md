# Deployment preparation — not deployed

The actual deployment host/domain is not selected or authorized. `deploy/*.example` and `backend/gunicorn.conf.py` are reviewable single-host examples, not installed services. They preserve SQLite, Django Admin and local private storage. Gunicorn is pinned; [official configuration reference](https://gunicorn.org/reference/settings/) supports the private bind, worker and timeout settings. Nginx/systemd execution remains unverified on a target host.

## Local review

Use the README safe-demo commands. Normal settings still target the untouched original database unless DATABASE_PATH is explicitly set; new publication APIs fail closed before approved migration. Do not run a real `migrate` merely to make the demo work.

## Required production configuration

Provision only after authorization: a persistent single-host filesystem, TLS domain/certificate, unprivileged service account, secret environment outside Git, private media/data directories and a separate backup destination. Use DJANGO_ENV=production, DEBUG=false, a fresh high-entropy SECRET_KEY, explicit ALLOWED_HOSTS, DATABASE_PATH, PRIVATE_MEDIA_ROOT, STATIC_ROOT and CSRF_TRUSTED_ORIGINS. CORS remains empty for same-origin use. Set SUPPORT_EMAIL only to a real monitored address.

For the supplied loopback proxy: TRUST_PROXY_SSL=true and TRUSTED_PROXY_IPS=127.0.0.1; the proxy must overwrite X-Forwarded-Proto/X-Real-IP and the app listener must stay private. Review certificate/domain/paths and copy proxy include to the configured location. Do not expose `.env`, database, backups, media, docs, source or legacy backend. Collect Django static files to a separate public static directory; serve only frontend `dist/` at root. Keep AI_ENABLED/AI_GUEST_ENABLED false until the model/rates/cap and live evaluation are approved.

## Controlled release sequence

1. Freeze editorial writes, create a private consistent backup using `backup_prepal`, restore into a new directory and compare database/media manifests.
2. Inspect 0005 SQL; run `verify_migration.py` against the restored copy. Review the no-backfill/publication-empty result.
3. Obtain explicit authorization to apply 0005 to the real database. Only then execute migration using the approved environment. Preserve the backup and prior compatible artifact. Do not reverse-migrate or overwrite newer writes casually.
4. Build assets, collect static files, create named editor accounts, review/publish the real unit. Configure a bounded scheduled `process_resources` invocation; process candidates outside HTTP requests. The example command is at most 20 candidates with bounded retries; schedule frequency/host memory must be measured.
5. Install/review private Gunicorn + Nginx/systemd examples. Verify HTTPS redirects, Admin login/CSRF, private media denial, proxy identity, CSP/PDF worker rendering, body/rate limits and `/api/health/`.
6. Execute target-host browser/load/parser checks, actual backup restore rehearsal and accessibility/content review. Verify provider cap/live quality separately if enabling AI.
7. Obtain explicit public deployment approval before exposing the service.

Backup example (after selecting private destination): from backend, `.venv/bin/python manage.py backup_prepal /absolute/private/new-backup`. Restore with `backend/.venv/bin/python scripts/verify_restore.py BACKUP NEW_RESTORE_DIRECTORY`. Freeze concurrent editorial/file writes; database backup is consistent but database/media coherence needs that operational freeze. Define retention/off-host storage and recurring restore checks before launch. The local temporary backup proves mechanics, not durable disaster recovery.

Current local proof: 20 tables and zero media files verified on backup/restore; migrated copy preserved 436 old rows, integrity and FK checks. Real migration is pending. No production service, infrastructure, DNS, certificate, spend or external exposure was created.
