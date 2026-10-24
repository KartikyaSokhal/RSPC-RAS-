# Free Render demonstration — approved main release, 24 October 2026

Use only existing [RSPC-RAS- Web Service](https://dashboard.render.com/web/srv-dbe6d5vb9u1s738ikh80/settings) and [prepal-staging-db](https://dashboard.render.com/d/dpg-dbe7a1oae00c73c5g090-a/info) under kartikyasokhal28@gmail.com. Both are Free/Singapore in the existing Prepal project. The database is PostgreSQL17/Available in the project's db environment and expires23November2026; web is in Staging. The publication task disabled auto-deploy; no resources, permissions, secrets or other service settings were changed. No paid upgrade, new purchase or persistent disk is needed for this **synthetic, text-only demonstration**. It cannot hold valuable data or uploads.

The service tracks main, with auto-deploy now Off (saved and verified before publication), repository root, bash deploy/render-build.sh and bash deploy/render-start.sh, health/api/health/. Latest completed failure stopped at core.staging_settings environment guard before DB access; subsequently inspected flags are production/staging and verify-full/internal hostname. Do not label that historical failure an observed TLS failure. No successful hosted React/API/health result exists yet. Only auto-deploy Off and a conditional start-command switch are authorized. No redeploy, live environment/secret edit or DB write is authorized. The start switch is deferred: current PREPAL_ENVIRONMENT is staging, POSTGRES_HOST is internal, and PREPAL_FREE_DEMO/PREPAL_FREE_DEMO_SYNTHETIC_DATA are absent. Do not falsely acknowledge an unaudited target as synthetic.

## Prepared separate profile

Start command to save only after all prerequisites below are verified: `bash deploy/render-free-demo-start.sh`. Existing build remains `bash deploy/render-build.sh` and never migrates or seeds. This selects core.free_demo_settings without changing production/staging/database policy modules.

| Configuration | Required for this demo only |
|---|---|
| DJANGO_ENV / DEBUG |production / false; normal strong key and explicit host validation apply |
| PREPAL_ENVIRONMENT |free-demo |
| PREPAL_FREE_DEMO / PREPAL_FREE_DEMO_SYNTHETIC_DATA |1 /1, explicit acknowledgement of disposable synthetic target |
| SECRET_KEY / STAGING_ACCESS_USERNAME / STAGING_ACCESS_PASSWORD |Retain existing private values; no rotation in this task |
| POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_PORT |Retain existing private connection values |
| POSTGRES_HOST |Exact external hostname: dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com |
| POSTGRES_SSLMODE |verify-full; require/disable/verify-ca are refused |
| POSTGRES_SSLROOTCERT |Existing trusted CA file when configured; otherwise pinned certifi CA bundle |
| ALLOWED_HOSTS / SITE_ORIGIN |Exact Render hostname / matching HTTPS origin; no wildcard/CORS expansion |
| PRIVATE_MEDIA_ROOT |Existing variable preserved but not used for any files in free profile |
| STUDENT_FEATURES_ENABLED / AI_ENABLED / AI_GUEST_ENABLED |Always false, even if environment attempts an opt-in |

The start script disables dotenv loading and selects only this profile. Secure host-only cookies, CSRF/HTTPS/HSTS policy and the independent staging Basic password barrier remain. Only healthGET/HEAD bypasses the barrier. No private credentials are logged, copied into source or embedded in frontend variables. New profile disables outbound email/Google/Gemini, and does not permit the staging student-test escape hatch. Admin login/logout for synthetic staff may use database sessions; content-changing Admin methods and every multipart request return403 before file parsing. Default media storage rejects direct saves/opens/deletes. No upload directory or ephemeral user database is created. Static build assets are regenerable; text sample content stays in the designated disposable PostgreSQL target after separate initialization approval.

## TLS and actual connectivity evidence

Render [internal TLS](https://render.com/docs/postgresql-creating-connecting#ssl-modes-for-internal-connections) uses self-signed certificates and cannot satisfy verify-full. We did not weaken that policy. The external endpoint actually passed trusted CA and hostname verification with TLS1.3, cipher TLS_AES_128_GCM_SHA256, using PostgreSQL SSLRequest negotiation. This proves network reachability and certificate validation from the local machine; it does not prove a web-service-origin connection, database authentication, schema or role permissions. No SQL or live DB write was performed. Browser-redacted credentials cannot be used as a connection string; do not try a placeholder or print passwords. A private existing environment file is required to complete authenticated read-only SELECT/version/schema/count checks. No root cause is inferred from an unperformed authenticated query.

Current inbound rules include0.0.0.0/0. This local-only task leaves them unchanged; narrowing needs an approved live network configuration change and appropriate service/operator addresses. Do not disable certificate verification or open further access to troubleshoot. The profile refuses an internal host rather than silently selecting require mode. No TLS exception is proposed because a verified external endpoint is available.

## Acceptance and free-tier limits

[Free Render limits](https://render.com/docs/free) include idle spin-down, ephemeral web files, no disk/SSH/Shell/one-off jobs and a30-day expiring free database. Outbound/public-database traffic can also lead to suspension. Render may bill bandwidth/build overages if a payment method is present; inspect account usage/spend policy before live redeploy, without automatically changing plans/payment settings. The owner permits no purchases/upgrades. Production30-day encrypted-backup requirements remain unchanged and are not met by this expiring demo; no production data is permitted here.

Current live DB contents, migration state and accounts are unverified. Before a separately approved initialization or deployment: read-only audit the exact database; confirm disposable/synthetic intent and absence of valuable records; review empty-target migrations0001–0012 and safe synthetic seed procedure; preserve existing secrets; deploy only reviewed code/profile. No in-build or automatic startup migrate/seed is provided. Health checks return503 on missing schema/connectivity and200 only when the publication table is readable. Keep Admin content changes disabled and learner/AI off. Verify hosted HTTPS/access/CSRF/assets/notes/practice and read-only DB after separate approval. Do not report local SQLite browser tests as live PostgreSQL acceptance.

One read-only HTTPS request to https://rspc-ras.onrender.com/api/health/ timed out after12seconds. Free-tier spin-up may take longer; do not infer a permanent outage or claim API readiness. The new profile passed local Gunicorn/React/Admin/static/health checks against a newly generated synthetic SQLite fixture only.

---

# Staging release publication authority — 23 October 2026

Owner approved the reviewed staging candidate for commit/normal push to the existing codex/prepal-1-0 branch, subject to final index/diff/secret checks. Source matched the259-file approved manifest; no application changes were added by this publication task. Verify the pushed SHA and its CI run before any future infrastructure step. This approval does not authorize Render permission expansion, paid services, production deployment or real database cutover. Prior approval states below are historical.

## Repository-specific Render GitHub access instructions

1. Sign in to Render using kartikyasokhal28@gmail.com. Select My Workspace (tea-cv4hdkqj1k6c73bk2a50) and reuse [Prepal / Staging](https://dashboard.render.com/project/prj-dbdmln3ncjis73anntfg). Do not create another account, workspace or project.
2. Sign in to GitHub as KartikyaSokhal with repository administration rights. Open [Render app installation settings](https://github.com/apps/render/installations/new) and configure the EXISTING KartikyaSokhal installation. If a different account/organization or a new installation is proposed, stop and verify identity rather than broadening access.
3. Under Repository access choose **Only select repositories**. Preserve the existing three repository selections that support other services, and add only **KartikyaSokhal/RSPC-RAS-**. Do not select All repositories, remove existing access or create a personal access token. Review the Render app's fixed requested permissions; adding a repository exposes that repository to the installed app, so obtain the owner's separate permission-change approval before Save.
4. Save only the approved repository-access change. Back in the designated Render account, refresh the existing GitHub credential's repository picker and verify the exact private repository appears. This task prepares instructions and does not perform Save or grant access.
5. After successful CI and separate infrastructure approval, select codex/prepal-1-0, repository root, exact reviewed commit, prepared build/start commands and auto-deploy Off. Do not select main or trigger a service creation/deploy/payment while merely validating access. Do not change repository visibility, upload secrets, or provision resources to test the picker.

These steps follow [Render's Git-provider configuration guidance](https://render.com/docs/git-provider#fixing-github-app-permissions). The integration was previously restricted to three other repositories; repository ownership/admin access alone does not grant Render access. No GitHub or Render permissions were changed by publication preparation.

---

# Render staging preparation — 23 October 2026

**Actual non-billable dashboard action:** created [Prepal project](https://dashboard.render.com/project/prj-dbdmln3ncjis73anntfg) with the empty Staging environment evm-dbdmln3ncjis73anntg0 in the verified workspace. Verified zero services and zero environment groups. This is an organizational container, not a running deployment; no charges, credentials or data were added. Reuse this project on the next turn.

**Prepared locally, not provisioned or deployed.** Current and remote branch `codex/prepal-1-0` remain at `8ef43c7e945d8d81d232b44583990b69f82519ff`; the student platform and this deployment candidate are uncommitted. No commit/push, paid resource, migration of existing data or real cutover is authorized. The owner approved restoring the sanitized root `.env.example`; the prior missing-template blocker is resolved. Historical sections below describe earlier approval states.

## Account and architecture decision

Authenticated browser verification: Render account `kartikyasokhal28@gmail.com`, sole Admin in My Workspace (`tea-cv4hdkqj1k6c73bk2a50`), Hobby workspace. Existing project My project contains SkillIntel services; an ungrouped medvice service also exists. No Prepal service/database was found. Preserve unrelated services. The Render GitHub connection is KartikyaSokhal but exposes only three repositories; `KartikyaSokhal/RSPC-RAS-` is absent. Grant access to that exact repository only after owner approval; do not broaden to all repositories. GitHub connector confirms it is private and owner has admin access.

Vercel browser and connector both identify the designated email. Existing Hobby workspace kartikyasokhals-projects has medviceplus-survey, dr.-sunaina and skill-intel-ui, not Prepal. Its connector lacks workspace scope, but browser access works; no reconnection is needed. Owner confirmed a client/commercial product. Vercel Hobby is therefore unsuitable under its [fair-use policy](https://vercel.com/docs/limits/fair-use-guidelines).

**Selected staging candidate: one Render Python Web Service serving built React, Django Admin, API and collected static files, plus Render PostgreSQL17 and a private persistent disk.** Same-origin `/api` avoids third-party cookies, cross-domain CSRF and an additional proxy/provider. Render's [native runtimes](https://render.com/docs/native-runtimes) include Node/npm. This is a staging baseline, not a load-tested production design. Separate Vercel Pro can be reconsidered if a CDN frontend warrants its extra service/proxy/cost.

Pricing observed in the authenticated database form and public [pricing page](https://render.com/pricing): web512MB $7/month; PostgreSQL256MB $6/month plus1GB $0.30/month; private disk1GB $0.25/month. **Estimated base $13.55/month**, excluding tax, bandwidth/build overages and independent encrypted backup storage/monitoring. Workspace currently has $0 build-overage spend limit. Do not change it automatically. Database autoscaling remains disabled in the unsubmitted estimate. No purchase has occurred. Free PostgreSQL expires after30days and free web has no persistent disk; neither meets durable staging storage. Render Hobby PITR is3days, not the owner's approved30-day production backup retention.

## Exact proposed service configuration (not actual resources)

| Setting | Prepared value |
|---|---|
| Account/workspace | Designated email / existing My Workspace |
| Repository/branch | KartikyaSokhal/RSPC-RAS- / codex/prepal-1-0, only after approved release push |
| Service type/runtime/root | Web Service / Python / repository root (not backend or parent rpsc) |
| Region | Singapore for both web and PostgreSQL |
| Build | `bash deploy/render-build.sh` |
| Start | `bash deploy/render-start.sh` |
| Health check | `/api/health/` (read-only database readiness) |
| Auto-deploy | Off; select reviewed commit manually |
| Python/Node | Existing pins3.14.6 /24.22.0, npm11 |
| PostgreSQL |17, new empty staging database; restricted runtime/migration/backup roles |
| Disk |1GB mount `/var/data`, application private media `/var/data/private-media` |
| Network | Render-assigned HTTPS temporary domain; no custom domain/public launch |
| Runtime | One synchronous worker,90second timeout for existing60second PDF worker; no access-query/body logging |

No service name/domain has been reserved and no hosted URL is verified. Avoid duplicate creation by refreshing inventories before provisioning. The build installs hash-locked Python requirements, npm lockfile dependencies, builds React and collects Admin static assets. It never migrates, seeds, transfers data or creates users. The new core.static_build_settings deliberately cannot connect to a real database. Build and start remain separate from an explicitly approved migration action.

core.render_settings inherits the closed staging profile and requires private staging HTTP Basic access credentials. This barrier protects SPA/Admin/API/assets; it is independent of student authentication, strips its Authorization header before DRF, never adopts a student identity, disables indexing/caching and leaves only GET/HEAD health public. Exact SPA paths preserve API404s and deny private filesystem paths. WhiteNoise serves only dist and collected staticfiles; private media stays behind existing publication/authorization handlers. Secure host-only SameSite=Lax cookies, exact HTTPS SITE_ORIGIN/CSRF trust and empty CORS allowlist retain one origin. Normal staging/production remain closed. Render-only synthetic student acceptance can explicitly set PREPAL_STAGING_STUDENT_TESTS and PREPAL_STAGING_SYNTHETIC_DATA together, requires a prepal_staging_ database name and the mandatory private staging barrier, and never enables Google or AI. Use only after infrastructure/TLS acceptance; production remains forced off.

Render proxy HTTPS termination is configured only in the Render profile. Client IP forwarding is deliberately untrusted until Render header overwrite/IP topology is verified; the app currently groups proxied callers by peer address. Verify limiter behavior and Admin protection before enabling student access. The access barrier is not per-student login or MFA. Private staging credentials need secure owner distribution/rotation; never embed them in a URL or commit them.

## Environment names (values supplied privately after approval)

Runtime: `DJANGO_ENV`, `PREPAL_ENVIRONMENT`, `DEBUG`, `ALLOWED_HOSTS`, `SITE_ORIGIN`, `SECRET_KEY`, `STAGING_ACCESS_USERNAME`, `STAGING_ACCESS_PASSWORD`, `DATABASE_ENGINE`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_SSLMODE`, `POSTGRES_SSLROOTCERT`, `POSTGRES_CONNECT_TIMEOUT`, `POSTGRES_STATEMENT_TIMEOUT_MS`, `POSTGRES_LOCK_TIMEOUT_MS`, `POSTGRES_IDLE_TRANSACTION_TIMEOUT_MS`, `POSTGRES_CONN_MAX_AGE`, `PRIVATE_MEDIA_ROOT`, `PYTHON_VERSION`, `NODE_VERSION`, `PORT`. Start script selects `DJANGO_SETTINGS_MODULE` and `PYTHON_DOTENV_DISABLED` itself. Never reuse the retired historical key or local development credentials. Migration/backup role credentials are separate and must not be injected into the normal web process.

Staging test opt-in names: `PREPAL_STAGING_STUDENT_TESTS`, `PREPAL_STAGING_SYNTHETIC_DATA` (both unset by default; no activation performed).

Disabled/unconfigured integrations: `STUDENT_FEATURES_ENABLED`, `AI_ENABLED`, `AI_GUEST_ENABLED`, `GEMINI_API_KEY`, `AI_MODEL`, `AI_DAILY_BUDGET_MICRO`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`, `SUPPORT_EMAIL`. Existing adapters remain; no credential was uploaded and no external provider request was made. Google consent/callback and SMTP delivery remain unverified. Do not configure dummy credentials as working integrations.

## PostgreSQL TLS, schema and recovery gates

Render [internal database TLS](https://render.com/docs/postgresql-creating-connecting#ssl-modes-for-internal-connections) uses self-signed certificates and explicitly does not support verify-full. The repository's verify-full requirement is **unchanged**. Proposed connection: full external database hostname with trusted OS CA bundle and verified hostname, restricted to the web service's documented outbound CIDRs plus a temporary explicitly approved operator IP for setup. Verify the actual certificate/handshake before migration or student data. Remove broad0.0.0.0/0 access; do not silently use require/disable. If verified external TLS cannot be established, stop and review another provider or an explicit security-policy decision.

Apply0001–0012 only to a newly approved empty staging target using the separate migration role. Check runtime cannot CREATE/ALTER and backup cannot write; verify table permissions, sequence use, role memberships and TLS. Existing guarded postgres_ops commands refuse remote databases and must not be bypassed or mistaken for hosted provisioning. No schema/model change was introduced here. Do not transfer source SQLite/demo content until the owner selects data and authorizes transfer. Initial acceptance can use synthetic records in the new target, with no transferred credentials or fabricated academic approval.

Owner approved daily encrypted backups with30-day production retention. This approves the retention requirement, not a paid storage provider, scheduler installation, account deletion or real cutover. Plan daily coherent DB/media capture, native PostgreSQL17 pg_dump, client-side CMS AES-256-GCM, separate recipient key custody, off-host ciphertext+receipt storage, lifecycle30days, fresh26-hour monitoring/alerts and independent restore. RPO24h is the proposed daily schedule; RTO requires a timed hosted drill. Render [PITR](https://render.com/docs/postgresql-backups) is3days on Hobby/7days on Pro and does not replace30-day paired media backups. Existing local encrypted restore proof remains historical; hosted/off-host transfer and scheduler integration are not activated. Native Render PostgreSQL client version must be checked; do not dump17 with an older bundled client.

## Next gated sequence

1. Review release diff, restored template, security scan and local verification; explicitly approve commit/push. Current remote CI failed before this candidate; a new remote green run remains required.
2. Approve narrow Render GitHub installation access and the recurring resource estimate. Provision a NEW empty staging target only after approval; no valuable data transfer is implied.
3. Establish restricted roles, verified external TLS, mount/media permissions, private access credentials and actual host/CSRF configuration. Separate migration action on new staging; no migrations in builds or routine restarts.
4. Deploy the reviewed SHA and test actual HTTPS, access barrier, health, static/Admin/editor, publication/files/discovery/MCQs. After staging access/TLS/schema checks, explicitly enable only the synthetic Render test gate for the requested browser login/session/ownership/planner acceptance. Keep production closed.
5. Verify off-host30-day encrypted backup/restore and alert delivery, provider consent/SMTP, rate-limit proxy behavior, resource/load limits and academic review. Request separate production/cutover acceptance; no automatic launch.

---

# Deployment and recovery gates

No staging/production URL, host/domain or real PostgreSQL cutover is established. Student-platform changes are uncommitted over 8ef43c7. Existing deployment files are examples, not installed infrastructure. The retired historical development key must never be reused. See [security](SECURITY.md).

## Ordered approvals

1. Review local student-platform diff and verified evidence; separately authorize commit/push. Preserve history and check exact outgoing SHA/CI. Prior branch publication does not authorize this work's push.
2. Human academic/rights review of new lesson/MCQ/alias/relationship drafts in the isolated Admin. Explicit review/publication precedes production content selection. Synthetic engineering approvals are not transferable authority.
3. Configure Google consent/client/exact same-origin callback and SMTP on an approved test origin; verify live sign-in, collision/replay/logout and email reset delivery. Decide password-account email-verification policy. Keep STUDENT_FEATURES_ENABLED=false until migrations, security and acceptance are verified.
4. Approve Gemini provider/model/current rates/bounded test budget before live requests. Evaluate current-lesson-only grounding/refusal/citations and billing. Keep live AI off meanwhile.
5. Select source data and PostgreSQL target/roles/TLS; approve fresh coherent DB/media backup, restore/rollback rehearsal and explicit cutover. Never migrate the original SQLite or preserved demos in place. Apply 0009–0012 only to the approved target under that scope.
6. Approve hosting/domain/billing, durable private media, static/proxy/worker settings, monitoring and access policy. Stage and validate before separate final production approval.

Topic-note PDF export remains deferred and is not a prerequisite silently added to this implementation. Phone OTP needs a provider/cost approval. Production load, manual assistive technology/device checks, auth/limiter retention and SMTP/consent operations remain unverified.

## Existing host examples and prerequisites

Review deploy/nginx.conf.example, deploy/prepal-proxy.conf.example, deploy/prepal.service.example and backend/gunicorn.conf.py on the actual approved host. They are examples, not verified infrastructure. Django's listener is private loopback, behind a TLS reverse proxy. Set DJANGO_ENV=production, DEBUG=false, a fresh strong SECRET_KEY, explicit ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS, PostgreSQL credentials and POSTGRES_SSLMODE=verify-full with trusted CA. Runtime role must not be superuser/CREATEDB; separate approved migration role and bounded connection settings are required.

Vite builds the SPA for same-origin /api. Serve only dist/static assets with SPA fallback and suitable hashed-asset caching; never serve repository/private-media/.env/.git paths. Collect Django static files only in approved deployment scope. Align STATIC_ROOT and PRIVATE_MEDIA_ROOT with service/proxy locations; defaults differ from the examples. Private media requires persistent protected storage and reviewed application delivery, not a public directory alias.

Configure HTTPS, trusted proxy overwrite rules, secure cookies/CSRF/CSP/HSTS, upload/rate limits, controlled Admin access and health/monitoring/restart procedures. Logs omit query strings/request bodies/credentials. Validate real filesystem ownership, persistence, process limits and recovery independently of the developer Mac. No key belongs in VITE_* or a source file.

PDF processing may run 60 seconds while proxy/Gunicorn examples allow 40/45. Resolve and test execution/timeouts under approved production scope; runtime configuration is unchanged here. Uploaded-PDF reading is implemented; topic-note PDF export is not. Keep live AI off until approved model/non-thinking compatibility, pricing/caps/billing and factual/citation evaluation.

## Database and rehearsal

Source migrations 0001–0008 remain unchanged; 0009–0012 add student identity/visits/plans/attempt snapshots. Original SQLite is content 0004 and immutable; existing demos are preserved. Prior PostgreSQL schema/ID/foreign-key/sequence/publication transfer and migration reversal/restore proofs used disposable targets only. [DATABASE_SCHEMA](DATABASE_SCHEMA.md) holds rehearsal/configuration details. Never fake migrations or run cutover tools against a valuable original database. Only new disposable/review targets were migrated in this task; real cutover remains unapproved.

Future approved PostgreSQL tests must use explicitly named disposable loopback databases and the guarded --postgres runner; production credentials are forbidden. Local tmpfs/Docker success is not durable production backup.

## Backup, restore and rollback

Before approved cutover, freeze editorial/file writes and pair a coherent source/database/media backup. pg_dump snapshots do not freeze external media. Use matching native PostgreSQL clients, private environment credentials and a NEW private dump destination; native clients read PG* variables while Django uses POSTGRES_*.

Commands for a separately approved real environment (synthetic local restore was rehearsed):

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

## Local development does not approve production access

Normal production and development default STUDENT_FEATURES_ENABLED=false; the explicitly selected marked student demo is the local exception. PREPAL_DEV_API_ORIGIN only selects a development proxy and is ignored by build/preview. Keep production flags/credentials unchanged until authentication/security acceptance and separate release approval. No cutover or migrations were performed by the navigation restoration. Root .env.example was already missing at preflight; release manifest remains blocked pending owner review.

## New local encrypted recovery workflow (unactivated production)

Run only with explicitly designated disposable loopback prepal_local_/prepal_rehearsal_ databases. Use the limited backup.env and a public recipient certificate; keep the associated private key outside the backup destination. Use OpenSSL3+ and matching PostgreSQL native clients. Generate a local drill key/certificate privately with openssl req -x509 -newkey rsa:3072 -noenc; supply -keyout to an outside-repository private key, -out to the public cert and a local synthetic subject. Mode0600 key/0700 directories; production key custody must be independently approved (offline/password-manager/HSM choice, separate access and recovery copy).

```sh
backend/.venv/bin/python scripts/postgres_ops.py backup-local \
  --env-file "$PREPAL_PRIVATE_BACKUP_ENV" --pg-bin "$PREPAL_PG_BIN" \
  --media "$PREPAL_PRIVATE_MEDIA" --destination "$PREPAL_PRIVATE_BACKUPS" \
  --certificate "$PREPAL_RECIPIENT_CERT" --openssl "$PREPAL_OPENSSL3"
backend/.venv/bin/python scripts/postgres_ops.py status \
  --directory "$PREPAL_PRIVATE_BACKUPS" --maximum-hours 26
backend/.venv/bin/python scripts/postgres_ops.py retention-plan \
  --directory "$PREPAL_PRIVATE_BACKUPS" --days 30
backend/.venv/bin/python scripts/postgres_ops.py restore-local \
  --env-file "$PREPAL_PRIVATE_ADMIN_ENV" --pg-bin "$PREPAL_PG_BIN" \
  --bundle "$PREPAL_ENCRYPTED_BUNDLE" --private-key "$PREPAL_RECIPIENT_KEY" \
  --database prepal_rehearsal_recovery_new --new-directory "$PREPAL_NEW_RESTORE_DIRECTORY" \
  --openssl "$PREPAL_OPENSSL3"
```

Backup uses one exported repeatable-read DB snapshot for inventory and native custom dump. Media hashes are compared before/during/after pairing; any detected change fails. Production uploads should be immutable or frozen for a coherent snapshot; a database snapshot does not transactionally lock files. Ciphertext and success receipt have hashes; CLI returns nonzero and writes failed status when backup fails. A stale/missing/failed status makes health command nonzero; configure an external monitor to run at least hourly. Retention-plan only lists hash-verified old managed files; it NEVER deletes. Restore refuses existing target/output, reauthenticates encryption before extraction and restores/validates all rows/FKs/sequences/media to a new local target with new roles. Archive keys are never included in backups. Never use untrusted pg_dump input.

Daily UTC02:15 with persistence/jitter and failure logger are provided in deploy/prepal-backup.service.example, prepal-backup.timer.example and prepal-backup-alert.service.example. They are NOT installed or enabled. Review service user/paths/native versions and configure a separate health-age poll and verified failure alert delivery. The command deliberately refuses production; a separately approved production wrapper/permissions review must precede activation. A journald failure entry is not a delivered alert. No macOS/system service or cloud scheduler was changed.

Production requires approved durable off-host encrypted object storage on a separate failure domain, access/immutability/lifecycle policy, independent restore from that remote copy, private-key recovery and actual alert delivery. No provider/account/paid infrastructure is selected or provisioned. Off-host transfer is not implemented/configured; choose the owner-approved native storage/SSH tooling, send ciphertext+receipts only, pin host identity, and verify remote hashes/restore. Decide daily24-hour RPO versus WAL/PITR and measurable RTO. Do not claim production backup completeness from these local tools/templates.

Rehearse a verified copied source before cutover:

```sh
backend/.venv/bin/python scripts/rehearse_student_postgres.py \
  --admin-env "$PREPAL_PRIVATE_ADMIN_ENV" --sqlite-copy "$PREPAL_VERIFIED_SQLITE_COPY" \
  --media-copy "$PREPAL_VERIFIED_MEDIA_COPY" --new-directory "$PREPAL_NEW_DRILL_DIRECTORY" \
  --pg-bin "$PREPAL_PG_BIN" --openssl "$PREPAL_OPENSSL3"
```

The rehearsal creates new databases, applies0001–0012, compares IDs/rows/FKs/37sequence counters, proves owned data and sessions through two actual backend starts on8003, then encrypted native restore/corruption rejection. Preserve its private evidence and failed targets for diagnosis; do not reuse/reset them. Private source/migration/restore files contain sensitive material and are0700/0600; they are not a production retention service.

**Next real cutover approval packet:** select academically approved source/content (exclude synthetic staff/test approvals), identify target PostgreSQL17 host/roles/CA/media and fresh rotated production secrets; freeze writes and take a NEW verified paired backup; repeat migration/transfer/persistence/independent off-host restore and RPO/RTO evidence; request explicit configuration switch approval. On approval stop writes, switch only approved env/proxy/service, validate sessions/CSRF/ownership/admin/content, retain rollback source. If rollback is needed, preserve/reconcile post-cutover writes, restore paired backup to a NEW target and obtain approval before switching back. Never fall back to immutable original SQLite or discard new activity.

A future restore that must preserve existing sessions/signatures also needs the independently secured original application SECRET_KEY. Data dumps contain neither this configuration secret nor role passwords. Generated restore credentials use fresh defaults; restore the approved signing context separately, or explicitly accept invalidated sessions/reset/preview signatures. Never restore the retired historical key. Local signing-context portability was verified without printing any key.
