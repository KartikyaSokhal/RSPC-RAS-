## Current release authority — 23 October 2026

The owner approved committing and normally pushing the reviewed staging candidate to codex/prepal-1-0 after exact staged-diff and secret checks. This supersedes earlier Git-publication prohibitions for this candidate only. All259 reviewed source inputs matched their approved hashes at preflight; required student source/migrations are part of this reproducible deployment candidate. No unrelated changes may be included. Stop on unexpected secrets, divergence or critical CI failure. No force push, main merge, paid provisioning, production deploy, database cutover or billable Gemini request. Render access work is instructions only; do not grant new permissions under this batch.

---

# Prepal repository instructions

This directory is the application Git root; origin is `git@github.com:KartikyaSokhal/RSPC-RAS-.git`. Preserve the parent wrapper and its inactive Git backup. Read [handoff](docs/AGENT_HANDOFF.md), [status](docs/PROJECT_STATUS.md), [scope](docs/MVP_SCOPE.md), [roadmap and checklist](docs/IMPLEMENTATION_PLAN.md), then relevant API/Admin/security documentation before edits.

## Current authority

Latest scope: local Render staging preparation and account inspection; commercial/client use is confirmed. Single-origin Render web/PostgreSQL/private disk candidate is prepared. No paid provisioning, commit/push, valuable data transfer or public launch without separate approval. Read the current DEPLOYMENT and top handoff before acting. Previous PostgreSQL preparation scope: The active8002 student-review backend remains SQLite; no actual cutover is authorized. New local loopback PostgreSQL rehearsal targets and synthetic tests are authorized, including fresh schema0001–0012, ID-preserving transfer, separate roles, backend restart and encrypted native independent restore. Preserve all uncommitted work and existing data. No commit/push/deploy, production activation, paid service or original/demo migrations. Irreversible account deletion and retention expiry require explicit owner approval; the new account/deletion endpoint is readiness-only and never deletes data.

Normal development and production default STUDENT_FEATURES_ENABLED=false. Only explicitly selected ready core.student_demo_settings or a separately configured core.local_postgres_settings candidate may enable the local workflow; keep production closed pending security acceptance. OAuth credentials and outbound recovery email require owner configuration; verify with mocks first. Live Gemini needs separate provider/model/request-budget approval. Preserve every existing database/media/private archive and migrations 0001–0008. New reversible migrations may run only against disposable targets or NEW isolated review environments.

## Application and data boundaries

Keep React/Vite, Django/DRF, Django Admin and PostgreSQL as the normal database. SQLite is only the immutable original archive or explicitly isolated test/demo backend. Preserve all original IDs/slugs/records/media, migrations 0001–0008, demo databases, credentials, private recovery/evidence and legacy learner records. No reset, clean, data rewrite or automatic fallback to original SQLite. Inspect existing databases only through read-only URI connections.

Student APIs must remain constant unavailable responses when STUDENT_FEATURES_ENABLED=false; when enabled, restore CSRF/session authorization and user ownership together. Never adopt ownerless records. Admin staff authentication and superuser staff-account management remain. Public reading/search/files/practice require current publication/review eligibility. SafeHtml is the browser HTML boundary; AI uses raw-HTML-disabled SafeMarkdown. Never fall back to drafts.

Content linking preserves stored HTML and evidence-bound editorial decisions. Analyze in Admin/management workflows, never student GET. Revalidate snapshots/revisions, approved proposals/aliases/tags, target and ancestor publication. Use the reviewed canonical collection service for public practice, never its draft-inclusive Admin counterpart. Grading stays deterministic; guest checks remain stateless and enabled owned submissions save immutable snapshots.

UI requirements are in ARCHITECTURE: preserve original unfiltered hierarchy numbering and slug routing, all-node/root-only expansion, honest statistics, existing light/dark tokens, accessible popups and one bottom-right Tutor launcher. Enable learner controls only with owned endpoints and the server gate. Enforce current-lesson-only Tutor. Topic-note PDF export is outside the current request.

## Verification and release hygiene

Use `backend/run_tests.py` with isolated configurations, mocked AI and synthetic data. Never point it at real data. PostgreSQL tests need a specifically approved disposable local target. Run migrations/preparation only against explicitly new disposable databases; never migrate existing application/original/demo files. Report actual passes/skips/limits and distinguish local/mock checks from remote/production evidence. Never print prompts, records, keys or passwords.

Existing sample setup is documented in README. Future preparation uses a NEW private destination, refuses existing paths/symlinks/populated databases, and must not reset a failed/manual demo. Engineering review flags are not human academic/rights approval. The verifier uses query-only mode. Preserve existing demos and media.

Canonical docs stay trackable; private history/evidence/design/proposals, databases/.env/media/dependencies/output stay excluded. Run `scripts/check_docs.py --release`, `scripts/release_manifest.py`, diff and secret checks before proposing a release. A worktree export is not a commit. Use the existing documentation index instead of recreating redirect files or duplicate handoffs. Keep significant decisions in DECISIONS/CHANGELOG; private archives retain complete originals.

## Local student startup

The active approved student frontend is http://127.0.0.1:5173, backend127.0.0.1:8002. Its PREPAL_DEMO_ROOT is the ready student-review path in AGENT_HANDOFF, not .local/demo. scripts/run_student_dev.py validates marker/schema read-only; never automatically prepares or migrates. npm run dev:student is cold start; --backend-only reuses managed Vite. Ignored .env.local uses PREPAL_DEV_API_ORIGIN only in development; normal build/preview routing is unchanged. Backend /api/config/ remains authoritative. Google stays disabled unless a separately configured/accepted environment supports it.

Owner explicitly approved restoring a sanitized root .env.example during staging preparation; release completeness is no longer blocked by that deletion. Preserve all other pre-existing work. Verify the complete release manifest before any approved Git operation.

## PostgreSQL operations guardrails

Use scripts/postgres_ops.py with owner-only environment files outside the application; never print credentials. provision-local/restore-local refuse remote/non-prefixed/existing targets. Migration role owns schema; runtime has table CRUD/sequence use only; backup is SELECT-only. Normal app cannot provision databases. core.staging_settings/core.production_settings require matching explicit profiles and force learner/AI/Google off pending acceptance. Production TLS requires verify-full/trusted CA. The private native16.2 test runtime lacks SSL: no production TLS or PG17 acceptance claim.

Use scripts/rehearse_student_postgres.py only with a verified source COPY and NEW private directory. It creates synthetic accounts/content in disposable PostgreSQL, not the active app. Encrypt paired DB/media with CMS AES-256-GCM; local recipient key stays private. Retention-plan is nondestructive; no scheduler/off-host monitor is enabled. Do not install example systemd units or treat them as durable production recovery. See DEPLOYMENT/SECURITY for remaining approval gates. Root .env.example was restored with owner approval. Daily encrypted30-day production retention is approved as a requirement; paid backup storage, scheduler activation and real cutover are not.

Render-only staging acceptance may explicitly opt into synthetic students using PREPAL_STAGING_STUDENT_TESTS plus PREPAL_STAGING_SYNTHETIC_DATA and a prepal_staging_ database, behind the mandatory private staging barrier. Do not use valuable data or activate production. DRF3.18.2/certifi2026.10.19 are now security-pinned; preserve both hash locks.
