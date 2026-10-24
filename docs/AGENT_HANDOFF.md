# Current handoff — approved staging branch publication

23 October 2026. Owner approved the reviewed candidate for one release commit and normal push to codex/prepal-1-0 in the private KartikyaSokhal/RSPC-RAS- repository. Base local/remote SHA was8ef43c7e945d8d81d232b44583990b69f82519ff with zero divergence. Every259 reviewed release input matched its approval hash before documentation updates. Source/application files are unchanged from that tested candidate. The commit containing this handoff is the staging release commit; resolve its exact SHA with `git log -1 --format=%H -- docs/AGENT_HANDOFF.md`, and verify remote branch equality before subsequent operations.

Publication must pass exact index-versus-release-manifest checks, private-artifact/known-secret/retired-key checks, redacted Gitleaks scan and git diff --cached --check. CI for the new commit must be inspected after push. A prior failed run at8ef43c7 is historical; do not claim the newly published candidate passed until its own run succeeds. Final remote SHA/run/job outcomes are reported in the task and private publication receipt; future agents must re-read the current branch Actions result rather than assume success. Stop on new critical failure without further implementation or publication.

Only use the existing Render Prepal project prj-dbdmln3ncjis73anntfg / Staging evm-dbdmln3ncjis73anntg0 in workspace tea-cv4hdkqj1k6c73bk2a50, account kartikyasokhal28@gmail.com. No compute/database resources or credentials are provisioned in this release task. DEPLOYMENT contains the exact least-privilege Render GitHub installation instructions: add only this repository to the existing installation while preserving the existing selections. Permission expansion is not executed by this batch.

Exact next task after successful CI: obtain separate approval for the narrow Render repository-access change and paid staging resources. Then configure a NEW empty PostgreSQL17 target with restricted roles/verified TLS, protected persistent media and staging access before an approved staging migration/deploy. No real data cutover, production launch, main merge, paid AI or learner production activation. Existing0012 migrations are included as source only. Original databases/media/private recovery remain local and unchanged. Earlier handoff sections are historical.

Private publication recovery/evidence: /Users/kartikyasokhal/Downloads/MYPLACE/rpsc/.recovery/prepal-staging-publication-eza12s7q. It contains the hash-verified reviewed-candidate archive and final staged/publication receipts. Do not publish it. Local verification carried forward from the exact tested source:90frontend tests/lint/build,204backend passes/five PostgreSQL-only skips,15public+five student Chromium, clean-export Render build, Gunicorn smoke and clean dependency audit. This documentation-only publication preparation does not claim a new hosted verification.

---

# Current handoff — Render staging candidate, 23 October 2026

**Actual non-billable dashboard action:** created [Prepal project](https://dashboard.render.com/project/prj-dbdmln3ncjis73anntfg) with the empty Staging environment evm-dbdmln3ncjis73anntg0 in the verified workspace. Verified zero services and zero environment groups. This is an organizational container, not a running deployment; no charges, credentials or data were added. Reuse this project on the next turn.

Branch codex/prepal-1-0; local and remote HEAD8ef43c7e945d8d81d232b44583990b69f82519ff unchanged. No compute/database resources or deployment URL, commit, push, paid request or real database operation. Preserve ALL earlier student-platform/PostgreSQL work. Verified recovery of250 pre-task files is at ../.recovery/prepal-staging-prep-fz4zfwdz/source-before.tar.gz; before.json/Git inventory and protected hashes accompany it.

Owner confirmed commercial/client use and approved restoring the sanitized root.env.example. Vercel Hobby is unsuitable; selected candidate is single-origin Render Python web serving React/Django/Admin plus PostgreSQL17 and private disk. Both browser identities match kartikyasokhal28@gmail.com. Render sole-Admin workspace tea-cv4hdkqj1k6c73bk2a50 exists; no Prepal service found. GitHub repo is private/admin-accessible but Render's installation exposes only3other repos and requires approved access expansion. Vercel project listing works in browser despite connector scope403. Existing unrelated infrastructure unchanged.

New source: backend/core/render_settings.py, render_urls.py, render_support.py, static_build_settings.py; deploy/render-build.sh, render-start.sh, render-gunicorn.conf.py; backend/content/test_render.py. Existing files changed this batch: root.env.example restored; requirements.in/two hash locks add WhiteNoise6.12.0 and patch verified advisories with DRF3.18.2/certifi2026.10.19; release_manifest requires deployment inputs. TutorPanel now exposes a focusable labelled conversation log and e2e/ui-foundation checks it, fixing the actual remote CI scrollable-region-focusable failure. Existing canonical docs updated. Full exact per-task inventory/final evidence is private; no source is staged.

Default settings force student/Google/AI off; Render-only explicit synthetic student-test flags require a prepal_staging_ database and never affect production. Settings require separate staging HTTP Basic access and secure same-origin cookies/CSRF. Build has no real DB access or migrations. Static collection/runtime are explicitly separated. Existing migrations0001–0012 and original/demo data unchanged. Render internal TLS cannot satisfy verify-full: preserve strict policy, verify external hostname+CA+restricted CIDRs before DB use. No real credentials entered into a dashboard. Budget proposal$13.55/month base plus backup storage/overages/tax; no payment authorization. Daily encrypted30-day production retention requirement is approved; hosted backup provider/scheduler/alerts/restore remain unimplemented/unactivated. Account deletion remains disabled.

Exact next task: review this candidate and obtain explicit local commit/push, narrow Render repository-access and paid staging approvals. Then provision only new empty staging resources, verify roles/TLS/media/HTTPS/access controls and migrations before deployment. Run actual hosted acceptance; synthetic student tests may use the explicit Render-only opt-in after TLS/schema/access checks; production remains closed. Do not invent URLs or report local tests as hosted results. Verification:204backend passes/5PG-only skips;90frontend tests/lint/build;15public+5student Chromium;real loopback Gunicorn routing/access/cookies/deploy-check;dependency audits clean after4advisory fixes.259release inputs and19release docs validate.16protected non-template hashes unchanged. Remote CI at8ef43c7 is still failed until a newly approved push/run. See DEPLOYMENT for exact configuration, TESTING for final results, SECURITY for unresolved controls. Earlier sections below are historical and must not override this scope.

---

# Current handoff — PostgreSQL student-data/security preparation

23 October2026. Branch codex/prepal-1-0; HEAD8ef43c7e945d8d81d232b44583990b69f82519ff unchanged, index empty. Preserve all earlier uncommitted student-platform/navigation work and pre-existing root .env.example deletion. No commit/push/deploy, real cutover, production secret change, irreversible deletion or paid API/infrastructure request. No model/migration changes in this task.

## Actual runtime and protected source

The approved UI remains http://127.0.0.1:5173 and student API8002, core.student_demo_settings, PREPAL_DEMO_ROOT=/Users/kartikyasokhal/Downloads/MYPLACE/rpsc/.recovery/prepal-student-platform-yeqsw05q/student-review. Actual engine SQLite, file demo.sqlite3, media sibling media/, schema0012. Preflight/final counts: auth_user1(synthetic staff), nonstaff/StudentIdentity/session/bookmark/progress/attempt/plan/task all0; Topic142/Question200/Choice800. Source integrity/FKs passed;26protected original/demo/review/environment hashes unchanged. Keep old8000 content-only service and Vite proxy unchanged. All original archives and existing demos/media/migrations remain preserved.

New task recovery: ../.recovery/prepal-postgres-security-d5oj1nit/. source-before.tar.gz contains239hash-verified pre-edit source/config/doc files; before/protected/git/preflight manifests retained. student-source-backup restored independently to student-source-restore (40SQLite tables including sqlite_sequence). Rehearsal used only that restored copy, not running source. All files are private; never publish archives, env/keys/dumps/logs. Retired historical key remains retired. No dependency installation/global PostgreSQL service was performed.

## Implemented and verified

core.database bounded timeouts/connection age; explicit core.local_postgres_settings, core.staging_settings, core.production_settings; production profiles remain learner/AI/Google off. Local provision creates only NEW approved loopback prepal_local_/prepal_rehearsal_ DBs, separate generated migration owner/runtime CRUD/backup read-only roles with no cluster-admin privileges or memberships and limits2/10/2. Private runtime and migration envs are separate; native backup env does not contain application SECRET_KEY. Production verify-full configuration/refusals are tested; real production17/TLS is not (native16.2 drill binary lacks SSL).

scripts/rehearse_student_postgres.py applies0001–0012 to fresh PG, preserves all39tables/2,433source rows/37sequence minima and FKs, then exercises synthetic account/password/session/bookmark/completion/visit/quiz/planner ownership. Two actual backend starts on8003 preserved the original test session and dashboard; immutable history and completed tasks survived edits/rescheduling. Runtime DDL/setval and backup writes were denied. Synthetic records stay in disposable targets.

postgres_backup and scripts/postgres_ops.py provide exported-snapshot native custom pg_dump + stable media, CMS AES-256-GCM, strict private env/files, authenticate-before-extract, trusted native pg_restore only to NEW local target and exact table/PK/FK/sequence/media validation. Final independent restore39tables/2,467rows/37sequences plus one test media file; restored original signing context validates session/password/history. Wrong key/tamper/truncation/CBC/traversal rejected. Actual documented backup/status/retention-plan/restore CLI passed. Private-key custody stays separate in production; preserve approved app SECRET_KEY securely across a future session-preserving restore (it is not in the data dump). New target role credentials/signing defaults do not automatically restore the old signing context.

Status/age command returns nonzero for missing/stale/failed backups; failure status/exit tested. Retention-plan only lists and never deletes. Daily UTC systemd/failure examples exist but are NOT installed/enabled or production-ready. No off-host storage, shipped ciphertext, remote recovery or delivered alert is configured. Production command deliberately refuses execution. Select approved service/destination/monitor, prove remote independent restore, key recovery and RPO/RTO before activation; daily logical backup is not PITR.

GET/POST account/deletion is readiness-only: caller-scoped counts, session+CSRF/current password/explicit confirmation/rate limits; valid POST409 deletion_policy_pending. No queued request, data deletion, session revocation or pruning occurs. SECURITY contains proposed7-day local/30-day production encrypted backup retention and personal-data erasure/session/deletion-ledger policy requiring owner approval; Google-only/staff workflows require separate handling. Registration availability still discoverable; SMTP/email-verification/abuse acceptance remains. No live Google/SMTP/Gemini.

## Results and remaining gates

204PostgreSQL passed (zero skips);204SQLite discovered/199passed/five PG-only skips;13new focused tests;90frontend/13files, lint/build;15public fixture +five student Chromium passed; Django check/migration consistency;26protected hashes. TESTING separates real PG/API persistence from SQLite/mock browser checks, actual evidence and initial fixture/path/public-schema/sandbox/trace-collision failures corrected without weakening boundaries. Local browser/axe is not physical/manual accessibility or production acceptance. Native16.2 temporary cluster is stopped after checks, with its private data/logs preserved; use a supported persistent approved local/host service for any future cutover.

Release blocker unchanged: root .env.example was already missing and blocks release manifest/--release doc check. Normal22doc validation passes. Do not restore it without resolving owner intent, claim a clean release export, stage/push or alter retired history. Gitleaks250candidate inputs had no findings;39current private values had zero exact source/bundle matches and retired values were not reintroduced. Scanners/private-value/preservation summary are recorded in TESTING; Git HEAD/index unchanged.

## Exact next task

Owner reviews local diff and approves deletion/backup-retention policy BEFORE irreversible implementation. Separately select the persistent PostgreSQL17 target, academic source/content and durable off-host backup/monitoring/key custody/RPO/RTO. Prepare a NEW frozen paired source backup and repeat migration/role/TLS/remote-restore/security acceptance, then request explicit actual connection/proxy cutover approval. Keep existing8002/UI unchanged until then. Do not transfer synthetic editor/test accounts or engineering publication approvals to production. Google/SMTP, public student activation, paid AI, Git release and deployment retain separate gates. No automatic next phase.

## Files changed in this task (relative to preserved pre-task working tree)

- `.gitignore`
- `AGENTS.md`
- `README.md`
- `backend/.env.example`
- `backend/README.md`
- `backend/content/services/postgres_backup.py`
- `backend/content/services/postgres_ops.py`
- `backend/content/student_auth.py`
- `backend/content/test_postgres_security.py`
- `backend/content/test_student_platform.py`
- `backend/content/urls.py`
- `backend/core/database.py`
- `backend/core/local_postgres_settings.py`
- `backend/core/production_settings.py`
- `backend/core/staging_settings.py`
- `deploy/prepal-backup-alert.service.example`
- `deploy/prepal-backup.service.example`
- `deploy/prepal-backup.timer.example`
- `docs/AGENT_HANDOFF.md`
- `docs/API_DOCUMENTATION.md`
- `docs/ARCHITECTURE.md`
- `docs/CHANGELOG.md`
- `docs/DATABASE_SCHEMA.md`
- `docs/DECISIONS.md`
- `docs/DEPLOYMENT.md`
- `docs/FEATURES.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/MVP_SCOPE.md`
- `docs/PROJECT_STATUS.md`
- `docs/SECURITY.md`
- `docs/TESTING.md`
- `scripts/postgres_ops.py`
- `scripts/rehearse_student_postgres.py`

---

# Current handoff — local student navigation restored

23 October 2026. Branch codex/prepal-1-0, HEAD8ef43c7e945d8d81d232b44583990b69f82519ff unchanged; all previous uncommitted work preserved. Root .env.example was already deleted before this task and is still missing: do not silently restore/remove it or claim release completeness. No commit/push/deploy, paid service, original-data change or migration.

Active UI: http://127.0.0.1:5173. Approved local student API: http://127.0.0.1:8002, core.student_demo_settings with PREPAL_DEMO_ROOT=/Users/kartikyasokhal/Downloads/MYPLACE/rpsc/.recovery/prepal-student-platform-yeqsw05q/student-review (already ready/schema0012). A legacy8000 service remains content-only. Ignored .env.local has PREPAL_DEV_API_ORIGIN=http://127.0.0.1:8002, read only in development; production preview/test origin priority is unchanged. Do not expose private .env.local or substitute a frontend learner flag. Normal development/production default closed; the explicitly selected marked student environment alone enables this workflow. Google remains disabled and SMTP is in-memory, not live delivery.

Current runtime uses `PREPAL_DEMO_ROOT=... npm run dev:student -- --backend-only`, reusing existing Vite. Cold start: select the same prepared root, `npm run dev:student -- --check` then `npm run dev:student` with ports8002/5173 free. Launcher validates read-only and never migrates or seeds; refuses production/unsafe/incomplete targets and cleans up only its own children. No original archive/old demo upgrade. See README for exact commands.

Navbar uses existing routes/menu: Search, theme, guest Sign In/Sign Up; authenticated Dashboard/named Account menu/Logout. Account state follows server sessions and config. All data APIs retain ownership/CSRF; no new Profile page or auth system. Source changes here are only routing/order, explicit default-off configuration and guarded startup plus regressions.

Tests:90 frontend/13files, lint/build passed;50 focused Django passed;full191discovered186passed/five PG-only skips;five student Chromium plus15existing fixture Chromium passed at320/390/768/1280 with login/logout/reload/guest dashboard, owned bookmarks/completion/planner, menu keyboard and both-theme axe. Actual5173 guest smoke passed without writing review data. No live provider or current PG test claim. Thirty-three protected original/review hashes unchanged; model/migrations0001–0012 untouched by this task. Earlier full-platform evidence below remains historical. TESTING records intermediate test fixes and release blocker.

Private new-task verified recovery/evidence: ../.recovery/prepal-auth-navigation-shqkfoqc/ (before.tar.gz, before/protected/git manifests and verification logs). Preserve the earlier full-platform archives as well. No secrets were printed in this task; credential literals remain absent from changed source/bundles. Existing root .env and backend/.env were not changed; only the ignored local frontend proxy configuration was added.

Exact next task: owner can use local email/password student flow at5173. Resolve the pre-existing .env.example release deletion separately before any release-completeness claim. Configure/test Google and SMTP only under approved service scope; keep production learner access off pending security acceptance. Preserve human academic review, production cutover, paid AI and Git/deployment approval gates. No automatic new module or release action.

## Files changed by this navigation task

- `AGENTS.md`
- `README.md`
- `backend/README.md`
- `backend/content/test_student_navigation.py`
- `backend/core/settings.py`
- `docs/AGENT_HANDOFF.md`
- `docs/ARCHITECTURE.md`
- `docs/CHANGELOG.md`
- `docs/DECISIONS.md`
- `docs/DEPLOYMENT.md`
- `docs/FEATURES.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/PROJECT_STATUS.md`
- `docs/SECURITY.md`
- `docs/TESTING.md`
- `e2e-student/platform.spec.js`
- `package.json`
- `scripts/run_student_dev.py`
- `src/components/layout/AppShell.jsx`
- `src/test/dev-routing.test.js`
- `src/test/student-navigation.test.jsx`
- `vite.config.js`

Private local-only addition: `.env.local` (ignored; development API origin only).

---

## Previous full student-platform handoff

# AI handoff — student platform

## Authority and repository

23 October 2026. Application root: Prepal/ inside the rpsc wrapper. Branch codex/prepal-1-0. Committed HEAD **8ef43c7e945d8d81d232b44583990b69f82519ff**. Origin git@github.com:KartikyaSokhal/RSPC-RAS-.git. Started clean; all changes below are uncommitted and unstaged. No commit/push/deployment/real PostgreSQL cutover/production secret change or paid API request is authorized. Previous presentation-cleanup proposal remains unapproved; no source/docs deletion or cosmetic move was executed.

Read AGENTS, PROJECT_STATUS, IMPLEMENTATION_PLAN, TESTING and relevant schema/API/security docs first. Do not revive older content-only restrictions for this locally authorized student implementation; do not infer production authorization.

## Recovery and protected data

Verified private pre-edit recovery: ../.recovery/prepal-student-platform-yeqsw05q/. before.tar.gz contains 365 pre-task files, individually hash-verified; before.json/protected.json/ARCHIVE_VERIFIED.json and Git baseline are retained. Never restore the retired Django key from any backup. No secret values may be printed.

28 protected original DB/media/env files remain byte-identical; original migrations 0001–0008 plus __init__ are unchanged. Original backend/db.sqlite3 remains content 0004; .local/demo and .local/sample-content-v1 remain 0008 and .local/demo-before-seed-proof remains 0005. Query-only integrity/FK checks pass for all four. Never migrate/reseed/reset them. Existing private recovery/evidence, media, dependency installations and Git history remain preserved.

New task-only review environment: ../.recovery/prepal-student-platform-yeqsw05q/student-review (schema0012, no student activity seeded). Start with PREPAL_DEMO_ROOT set to that absolute path and --settings=core.student_demo_settings; Vite uses PREPAL_API_ORIGIN=http://127.0.0.1:8002. See README for reproducible NEW destination preparation. This is synthetic SQLite/mock AI, not normal PostgreSQL runtime or production. student-browser/sample-browser/integration-demo-verified are separate mutable tests; partial failed integration-demo is retained for diagnosis, never reused/reset. Logs/dumps/credentials/inventories stay private.

## Implemented modules and source boundaries

1. student_auth.py reuses Django User/sessions/password hashing. StudentIdentity normalizes unique email/Google subject; Google state/nonce/PKCE/signed audience/issuer/expiry/verified email and no automatic linking. Reset tokens are single-use/30 minutes and fragment-based; SMTP failures remain generic. AuthRateWindow HMAC keys enforce rates. Normal production/development STUDENT_FEATURES_ENABLED defaults false; safe template explicitly false. Existing demo/test default stays closed; student_demo explicitly enables. Tests mock external exchange/mail, no mock-login bypass.
2–3. student.py/student_views.py provide owned dashboard/bookmarks/completion/visits. Eligible units are currently visible published notes or approved attached PDFs; structural headings excluded. Weighted accuracy uses all attempts; continue uses explicit visits. GET never writes; no NULL-owner adoption. Reader updates only after successful mutations; account changes discard private page state and refresh syllabus flags.
4. planner.py schedules owned StudyPlan/StudyTask deterministically: published branch selection, weekday/capacity split, approximate editor total estimate/default90 editable. Learn60/20/20%, quick revision half total/min15 split20/50/30%. Two-year/5,000-task bounds; revision409 for stale edits. Completed IDs/timestamps survive edits/rescheduling. Weekly subject minutes, monthly planned-unit/work completion and estimated end/exam feasibility are returned. Task completion is distinct from whole-lesson completion.
5. student_lessons_v2.json contains **25 new leaf lessons, 10,929 words (423–448 each), 125 MCQs/500 choices**, five per actual root, excluding all prior15 lessons. create_review_content validates mapping/tags/options/sources/idempotence and creates in_review notes, draft aliases/relations, unapproved quizzes, no new publication approval. Isolated review totals:142 topics/40 note blocks/40 quizzes/200 questions/800 choices/23 tags/40 aliases/102 relationships;30 old synthetic publications/15 old quiz reviews only. New IDs:32,34,38,39,49;56,66,69,88,89;92,94,99,105,106;109,110,111,113,114;125,126,127,130,131. Exact titles/path/source catalogue in ADMIN_WORKFLOW and private review-inventory.json. Human academic/rights/link/quiz approval is pending. Do not transfer synthetic approvals.
6. attempts.py reuses canonical grading/Question; immutable QuizAttempt snapshots preserve reviewed text/choices/answers/explanations/classification after edits/deletions. Per-user UUID idempotence, signed review revalidation and canonical row locks. Guest checks remain stateless. Own list/detail/weakness/subject-performance only; other users404. Legacy empty snapshots report detail unavailable. Quiz FK PROTECT retains history.
7. retrieval.py/tutor.py reuse Gemini and budget services but enforce current published note blocks only; no PDF/related/external evidence. Selection revisions, response manifests/publication and prompt overrides are checked. History cannot make an unrelated question relevant. Single responsive Tutor launcher retains selected/explain/summarize. Live AI remains off/no requests; mocks do not establish factual entailment or billing.
8–10. New migrations0009 identity/limiter,0010 visits,0011 planner/estimate,0012 practice snapshots. SQLite fields reuse existing sequence-preserving operation. Forward/reverse tested only disposable; reverse drops new module metadata and needs backup before any real use. source-copy migration preserved437 original rows/IDs/counters. Disposable PostgreSQL16.2 full tests, transfer and native restore passed; CI target17 is unrun for this work. New student browser suite and CI/release-manifest entries preserve all existing tests.
11. Existing canonical docs updated; no redundant documents created or historical files removed. Full file list follows.

## Verification and limitations

Baseline80 frontend/121 backend+four skips. Module focused checks13,17,24,30,49,26 passed in order. Final frontend86 tests/11 files, lint/build pass. Final backend185 discovered: SQLite180pass/five PG skips; PostgreSQL185pass/no skips. Chromium:15 fixture,9 integration,4 academic sample and3 student pass; desktop/mobile themes/automated WCAG scans, Admin publication/PDF/CSP, linking/popups/practice and cross-user isolation covered. No physical-device/manual screen-reader or production load claim.

Synthetic source transfer39tables/222rows, one media file, deleted-ID counters; native custom dump restore39tables/37sequences/FKs exact. Original-copy migration18tables/437rows conserved. Django system/migration consistency and independent eight-contender spend-race checks pass. Private exact log names and diagnosed intermediate failures are in TESTING. Final release/export/secret/data results are recorded below. No current remote CI result; prior base run39632028522 failed test:e2e, locally not reproduced and no assertion weakened.

Google credentials/consent and SMTP delivery require approved test-origin setup; password registration email verification policy remains open. Gemini needs explicit provider/model/current price/budget approval then live evaluation. Production remains gated pending real DB/roles/TLS/backup/cutover, media/proxy timeout alignment, hosting/domain/monitoring and final acceptance. Auth rate-window retention/pruning and production-scale planning/dashboard performance need operations review. Topic-note PDF export and phone OTP are deferred.

## Exact next task

Owner reviews current local diff and evidence. Next implementation activity is human academic/rights/MCQ/alias/relationship review of the new isolated corpus plus Google/SMTP acceptance on an approved test origin, **not automatic deployment or cutover**. If code issues emerge, fix locally with isolated regressions. Seek separate approval before paid Gemini tests, Git commit/push, actual data migration or deployment. Preserve the recovery and original data throughout.

## Changed and added files (working-tree release candidate)

- `.github/workflows/checks.yml`
- `AGENTS.md`
- `README.md`
- `backend/.env.example`
- `backend/README.md`
- `backend/content/models.py`
- `backend/content/permissions.py`
- `backend/content/serializers.py`
- `backend/content/services/providers.py`
- `backend/content/services/publication.py`
- `backend/content/services/retrieval.py`
- `backend/content/services/sample_content.py`
- `backend/content/services/tutor.py`
- `backend/content/test_ai.py`
- `backend/content/test_mvp.py`
- `backend/content/test_phase2.py`
- `backend/content/urls.py`
- `backend/content/views.py`
- `backend/core/demo_settings.py`
- `backend/core/settings.py`
- `backend/core/test_settings.py`
- `docs/ADMIN_WORKFLOW.md`
- `docs/AGENT_HANDOFF.md`
- `docs/AI_SYSTEM.md`
- `docs/API_DOCUMENTATION.md`
- `docs/ARCHITECTURE.md`
- `docs/CHANGELOG.md`
- `docs/DATABASE_SCHEMA.md`
- `docs/DECISIONS.md`
- `docs/DEPLOYMENT.md`
- `docs/FEATURES.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/MVP_SCOPE.md`
- `docs/PROJECT_STATUS.md`
- `docs/README.md`
- `docs/SECURITY.md`
- `docs/TESTING.md`
- `e2e-integration/journey.spec.js`
- `package.json`
- `scripts/rehearse_postgres.py`
- `scripts/release_manifest.py`
- `scripts/verify_postgres_transfer.py`
- `src/App.css`
- `src/App.jsx`
- `src/components/ai/TutorPanel.jsx`
- `src/components/layout/AppShell.jsx`
- `src/context/AuthContext.jsx`
- `src/pages/dashboardPage.jsx`
- `src/pages/infoPage.jsx`
- `src/pages/loginPage.jsx`
- `src/pages/quizPage.jsx`
- `src/pages/signupPage.jsx`
- `src/pages/topicPage.jsx`
- `backend/content/fixtures/student_lessons_v2.json`
- `backend/content/management/commands/create_review_content.py`
- `backend/content/migrations/0009_student_identity_and_auth_limits.py`
- `backend/content/migrations/0010_student_visits.py`
- `backend/content/migrations/0011_study_planner.py`
- `backend/content/migrations/0012_immutable_practice_history.py`
- `backend/content/services/attempts.py`
- `backend/content/services/planner.py`
- `backend/content/services/review_content.py`
- `backend/content/services/student.py`
- `backend/content/student_auth.py`
- `backend/content/student_views.py`
- `backend/content/test_review_content.py`
- `backend/content/test_strict_tutor.py`
- `backend/content/test_student_migrations.py`
- `backend/content/test_student_platform.py`
- `backend/core/student_demo_settings.py`
- `e2e-student/platform.spec.js`
- `playwright.student.config.js`
- `scripts/prepare_student_demo.py`
- `src/components/auth/GoogleSignIn.jsx`
- `src/pages/attemptPage.jsx`
- `src/pages/plannerPage.jsx`
- `src/pages/resetPasswordPage.jsx`
- `src/test/student-platform.test.jsx`

## Prior full-platform release verification (before navigation task)

The private clean worktree export contains **236 hash-verified required inputs** and no private artifacts. Fresh `npm ci --offline` and hash-locked Python installation succeeded; export backend185 discovered/180 passed/five PostgreSQL-only skips. Final frontend86 tests/lint/build are verified after the reset flow refresh/navigation fix. Dependency versions/lockfiles are unchanged. Source and exported inputs are compared byte-for-byte after documentation synchronization; this is an uncommitted worktree export, not a clean committed checkout or deployment.

Release and seven reachable-commit history Gitleaks scans passed with full redaction. Independent exact checks found zero current/retired values in release inputs and zero five-current-private-value matches in reachable Git blobs. One already-known retired historical credential blob remains; it is absent from the current local environment. A parser exception in the first exact-scan attempt echoed that retired historical value in tool output; the scanner was corrected to inspect constants without emitting values. No active credential was exposed or written to source, and no history was rewritten. Private exact-secrets.json records counts only.

All28 protected hashes, original migrations, four query-only SQLite integrity/FK checks, empty index/unchanged HEAD, diff whitespace and Git fsck pass. Documentation destinations pass for19 canonical release documents. No new remote/CI claim. The temporary synthetic PostgreSQL cluster is stopped after verification; retain its private data/dump/manifests, never use this disposable runtime for production.

Staging security audit initially found PYSEC-2026-4320 in certifi2026.10.18 and CVE-2026-114136/114137/114138 in DRF3.17.2. Updated to the upstream fixed certifi2026.10.19/DRF3.18.2 and regenerated both hash locks; final runtime advisory scan is clean. This required clearing Django's cached Authorization mapping after staging Basic authentication so patched DRF does not treat the separate staging credential as a student credential. No token-auth system was introduced.

This batch changed20existing files and added/restored9; none removed. Exact paths are in private task-changes.json beside source-before.tar.gz. Source model/migrations matched the pre-task hashes; index remains empty. Final fresh export successfully installed patched locked dependencies and ran the full documented Render build.
