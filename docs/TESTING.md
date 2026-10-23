# Approved staging publication checks — 23 October 2026

All259 release source inputs exactly matched the previously reviewed/tested manifest before publication documentation edits. Reuse the recorded90frontend/204backend+five skips/20Chromium/clean-export-build evidence for that source; no application change was made in this publication task. New checks cover exact staged diff, full index completeness, exclusions, redacted secret scanning including retired-key non-reintroduction, documentation links and normal remote branch equality. Inspect CI for the newly pushed SHA; prior failure at8ef43c7 is not evidence about this new commit. The final task report/private receipt records actual publication and CI results. Stop on critical failure. No tests or migrations against valuable databases, live AI requests or deployment are part of this batch.

---

# Render staging verification — 23 October 2026

**Actual non-billable dashboard action:** created [Prepal project](https://dashboard.render.com/project/prj-dbdmln3ncjis73anntfg) with the empty Staging environment evm-dbdmln3ncjis73anntg0 in the verified workspace. Verified zero services and zero environment groups. This is an organizational container, not a running deployment; no charges, credentials or data were added. Reuse this project on the next turn.

Current branch codex/prepal-1-0, local and remote HEAD8ef43c7e945d8d81d232b44583990b69f82519ff. Candidate remains uncommitted/unstaged; no hosted URL, provisioned resource, commit/push or real database migration. Protected original/demo data remains untouched. Prior results below are historical.

| Check | Actual result |
|---|---|
| Frontend lint/tests/build | Passed;90 tests across13files |
| Full backend after DRF3.18.2/certifi patch |209 discovered:204 passed,5PostgreSQL-only skips;14.665s |
| New Render regression coverage |5 tests included: fail-closed settings, synthetic-only opt-in, independent staging authentication, frontend and private path boundaries, static assets, Admin and secure cookies |
| Public Chromium |15 passed,35.9s; includes explicit keyboard-focus regression for remote CI issue |
| Student Chromium after patched DRF |5 passed,32.5s on newly created isolated fixture; signup/login/logout/session persistence/ownership/planner/MCQ and accessibility |
| Actual loopback Gunicorn stack |9 authenticated routes correct;4unauthenticated denials;health200;secure CSRF cookie;compiled SPA/Admin assets;process stopped |
| Django deploy/system checks |No issues using synthetic settings; not a hosted TLS/role acceptance |
| Migration consistency |makemigrations --check --dry-run: no changes; no original/demo migrations applied |
| Dependency audit |Initial4advisories remediated by DRF3.18.2/certifi2026.10.19; final pip-audit zero known advisories; npm runtime audit zero |
| Secrets |Gitleaks8.30.1:zero candidate and reachable-history scanner findings; separate exact historical-key comparison confirms1retired key in2commits, absent from candidate/inspected local envs |
| Data protection |16non-template preflight environment/database/media hashes unchanged; protected migrations/models unchanged from pre-task snapshot |
| Release/docs |259 explicit release files;19release Markdown documents validate; approved root.env.example restored; no private artifacts/known current credential matches |
| Remote CI |Run39632036431 at8ef43c7 failed2Chromium scrollable-region-focusable checks on.chat-messages; locally fixed with labelled focusable log; new remote run pending approved push |

Clean release-export build uses the documented Render command, fresh virtualenv/hash-locked pip install and npm ci. It builds React and collects159 static files/459postprocessed assets. Final fresh export also passed using the security-patched requirements; evidence lives privately at ../.recovery/prepal-staging-prep-fz4zfwdz/. This is local macOS reproducibility, not proof of Render's Linux runtime or hosted deployment.

Reproduce: npm run check; backend/.venv/bin/python backend/run_tests.py; npm run test:e2e; prepare a NEW private student fixture with scripts/prepare_student_demo.py then PREPAL_DEMO_ROOT pointing to it npm run test:student. Run browser suites serially. bash deploy/render-build.sh installs dependencies and produces assets; it never migrates. Use scripts/check_docs.py --release, scripts/release_manifest.py, git diff --check and redacted secret scanning. Never run tests against valuable data or publish private logs.

Intermediate diagnoses: sandbox blocked loopback binding until host-permitted Chromium run; uv cache required a task-private writable cache and registry access. After security patch, DRF read Django's cached Authorization header, causing1Render regression failure; middleware now invalidates that cache after stripping the independent staging credential, and all209tests plus real Gunicorn smoke pass. No security assertions were disabled. A broad historical-literal scan initially included the documented nonproduction placeholder; the refined retired-key check isolates the original Django-generated key without displaying its value.

Not verified: real hosted URLs/HTTPS/proxy IP overwrites, PostgreSQL17/verify-full handshake/roles, mounted durable media, off-host30-day recovery/alerts, live SMTP/Google/Gemini, Linux/load or manual-device acceptance. This batch did not rerun PostgreSQL-specific tests; prior PostgreSQL16.2 evidence remains below. Local Gemini key presence does not authorize use. Render learners default off; explicit synthetic-only acceptance requires both test flags, prepal_staging_ target and staging access barrier. Production learners/AI/Google remain closed.

---

# PostgreSQL student-data/security verification — 23 October 2026

Current local task over branch codex/prepal-1-0, HEAD8ef43c7e945d8d81d232b44583990b69f82519ff. All prior uncommitted work preserved. No original/demo DB migration, real cutover, production activation, account deletion, commit/push/deploy, dependency installation or paid request.

| Check | Actual result |
|---|---|
| Full disposable PostgreSQL16.2 Django | **204 passed, zero failed/skipped**,24.8s |
| Full isolated SQLite/in-memory Django | **204 discovered;199 passed, five PostgreSQL-only skips**,17.1s |
| New focused config/deletion/native crypto regressions | **13 passed**; included in both full suites |
| Frontend | **90 passed/13 files**; lint and production build passed |
| Chromium public/closed-gate/security/responsive fixtures | **15 passed**,35.7s |
| Chromium student integration on NEW SQLite fixture | **five passed**,33.2s; signup/login/logout/session reload, mobile/keyboard/themes/axe, owned data/planner/attempts, mocked Tutor |
| Django system check / makemigrations --check --dry-run | No issues; no changes detected on limited-role disposable PostgreSQL |
| Source SQLite backup/independent copied restore |40tables incl sqlite_sequence, zero source media; DB integrity/FKs passed |
| Current source-copy→PostgreSQL transfer |39application tables/**2,433 rows**/**37 sequences**, fields/IDs/FKs and migration metadata exact |
| Student persistence and backend restart | Two actual backend starts/termination on8003; persisted session and owned dashboard, immutable snapshot/planner completed history and password hash verified |
| Encrypted native independent restore |39tables/**2,467 rows**/**37 sequences** plus one synthetic media file; every table/column/PK hash exact; FKs validated; session/password/owned learning data usable |
| Least privilege and SCRAM | Runtime CREATE/ALTER/setval plus backup DELETE/CREATE rejected (five); all three roles non-admin/non-member with bounded connections; wrong password rejected for each |
| Native crypto and backup monitoring | Tamper/truncation/wrong key/CBC/traversal rejected; success/failure/missing status and nonzero CLI failure; review-only retention leaves files intact |
| Documented CLI | backup-local success; health healthy; retention dry-run; separate CLI restore39tables/2,467rows/37sequences |
| Protected data |26preflight DB/media/environment hashes unchanged; read-only SQLite integrity/FKs passed; original models/migrations and active8002 unchanged |
| Secrets/Git | Gitleaks8.30.1 scanned250existing candidate inputs: zero findings;39private values: zero exact matches in candidate/built assets; retired values not reintroduced; HEAD/index unchanged |
| Docs/release |22canonical local Markdown files validate; release validator and manifest remain **blocked by pre-existing missing root .env.example** |

Reproduction: backend/.venv/bin/python backend/run_tests.py; approved named loopback PG env + backend/run_tests.py --postgres; npm run check; npm run test:e2e; NEW prepared student fixture + npm run test:student. Never point tests at application data. Run browser suites **serially** because they share dist/test-results; use private new fixture roots. Use backend/README and DEPLOYMENT for private-env provision/CLI/rehearsal commands. OpenSSL3+ is required for CMS AES-GCM tests; native crypto class explicitly skips on unsupported runtimes rather than substituting unauthenticated encryption.

Evidence is private at ../.recovery/prepal-postgres-security-d5oj1nit/: source-before.tar.gz/before/protected/Git manifests, preflight.json, student-source-backup and verified student-source-restore, student-rehearsal-final/result.json and transfer.json, cli-verification.json, backup-security.json, backend-sqlite-final.log, backend-postgres.log, frontend.log, chromium-fixtures-final.log and chromium-student.log. Original source is ../.recovery/prepal-student-platform-yeqsw05q/student-review/demo.sqlite3; the rehearsal imports only its verified restored COPY. Failed earlier rehearsals remain preserved and are not reused.

Intermediate failures corrected/diagnosed: missing order in a synthetic content block stopped the first drill; backup-directory normalization initially treated a sibling ../ recovery path as inside the app; native restore initially attempted CREATE SCHEMA public although provisioning had already created it (now only that create entry is omitted). Source was never changed. A sandbox-only PDF regression failed its macOS ps monitor; host-permitted full rerun passed, without loosening resource limits or test assertions. Concurrent browser runs collided in Playwright trace artifacts (ENOENT), then serial public suite passed unchanged. No product bug was masked by disabling checks.

Environment limits: PG16.2 local binary has no SSL; production17/verify-full handshake/real CA and host hardening are NOT verified. Browser integration uses an explicitly isolated SQLite fixture with mock Tutor, while PostgreSQL persistence/restart/restore used real HTTP/API and native database checks. No live Google/SMTP/Gemini, production hosting/load/physical-device/manual assistive-tech or remote CI claim. Daily/off-host/alert/retention/account-deletion activation remain approval gates. Release export cannot be claimed complete while the root template is missing.

---

# Local student navigation verification — 23 October 2026

Current task reuses the existing uncommitted student implementation. Branch codex/prepal-1-0; committed HEAD8ef43c7e945d8d81d232b44583990b69f82519ff unchanged. No commit/push/deploy, paid request, model/schema change or migration/preparation command against any application database.

## Runtime and gate

The visible app was using core.demo_settings and correctly returning student_features_enabled=false. React already had the account routes/buttons; bypassing that backend gate would be unsafe. Normal settings now default learner=false in both development and production. The explicitly selected ready core.student_demo_settings enables the local owned flow, keeps real keys cleared and Google unavailable. Guest/account header order: Search, theme, Sign In/Sign Up or Dashboard/named Account menu/Logout. No new authentication system or nonexistent Profile route.

Active frontend http://127.0.0.1:5173 uses the explicitly selected student backend http://127.0.0.1:8002; public config returns learner=true/Google=false. A pre-existing content-only backend remains on8000 with learner=false. Ignored .env.local (0600) selects PREPAL_DEV_API_ORIGIN=http://127.0.0.1:8002. This override applies only to Vite development, even when an older shell exports PREPAL_API_ORIGIN=8000; production build/preview and explicit test origins are unchanged. Backend config/CSRF/session/ownership remain authoritative.

The selected database is ../.recovery/prepal-student-platform-yeqsw05q/student-review at schema0012. It was prepared in the previous task, not migrated/reseeded here. scripts/run_student_dev.py --check validates the ready marker and schema query-only. Cold start npm run dev:student binds8002/5173; --backend-only reuses already managed Vite. Launcher refuses production/unmarked/incomplete/symlinked/unmigrated destinations and never prepares/migrates. The backend-only launcher is currently running; it terminates only its own children when stopped. Use the README commands and this exact prepared root; do not turn on the old core.demo_settings gate.

## Actual results for this task

| Check | Result |
|---|---|
| Frontend unit/regression | **90 passed, 13 files** |
| Frontend lint / production build | Passed |
| Focused Django auth/local-startup/ownership/planner | **50 passed** |
| Full isolated Django | **191 discovered: 186 passed, 5 PostgreSQL-only skips** |
| Student Chromium | **5 passed**; guest/account navigation, signup, login after logout, reload persistence, CSRF/session ownership, bookmarks/completion/planner, guest dashboard401 and own empty-state prompt |
| Responsive / keyboard / themes | Student viewports320/390/768/1280; native menu Enter/Tab, visible logout, no horizontal overflow, light/dark automated WCAG2/2.1 A/AA checks with reduced motion |
| Actual running frontend | Read-only Chromium smoke at5173 confirms Sign In/Up, working login route, disabled Google and guest dashboard prompt; no account/data writes in the selected review DB |
| Django check / migration consistency | No issues; no changes detected; no original migrations applied |
| Protected data | **33 original/review file hashes unchanged**; prior uncommitted source outside this scoped change preserved |
| Documentation | Normal link validation passed; release-mode check/manifest blocked by pre-existing missing root .env.example |

Existing closed-gate/public-UI Chromium regressions: **15 passed (35.9s)**, including responsive 320/390/768/1024/1280 layouts. No PostgreSQL-specific suite or live Google/SMTP/Gemini was run for this navigation-only task; previous full-platform PostgreSQL results below are historical. Browser tests mutate only the separate student-browser fixture, not the active review/original/demo databases. Keyboard/axe/viewport emulation does not establish physical-device or manual screen-reader acceptance.

Intermediate failures: the first two new navbar axe tests sampled animated theme changes and failed contrast; they now use the same reduced-motion setup as existing student accessibility journeys and pass without changing colors or suppressing rules. The new proxy configuration unit test initially imported esbuild through the React plugin under jsdom; the config-only unit isolates that unrelated plugin, while the real production build still runs it. Old managed local services reappeared on their original ports, so the student API uses8002 and development-only explicit routing instead of repeatedly replacing those processes. No data/safety guard was relaxed.

## Preservation and remaining blockers

The deletion of root .env.example existed at preflight and is intentionally preserved; scripts/release_manifest.py and check_docs.py --release cannot validate a complete release until the owner resolves that separate deletion. No other deletion was introduced. Credential/database/media files and .env.local remain ignored/untracked; exact-value checks found no current private value in changed source or built JavaScript. No credential values were displayed. HEAD/index unchanged and no staged files. Private recovery before.tar.gz is verified, plus before/protected/git manifests and logs in ../.recovery/prepal-auth-navigation-shqkfoqc/.

Remaining authentication acceptance: configured/authorized live Google consent/callback and SMTP delivery, production email-verification/abuse policy and separate production security acceptance. Email/password signup/login/logout, persistent sessions and owned learner functions work in isolated tests and are exposed in the approved local environment. Production stays default-off; no external environment configuration was modified.

---

## Previous full-platform verification (historical)

# Testing and verification — student platform

Local verification over committed 8ef43c7, 23 October 2026. No new commit/push/remote CI, deployment, real cutover or paid provider call. Google/SMTP/Gemini are mocked. Existing source/data are protected by a verified private pre-edit archive at ../.recovery/prepal-student-platform-yeqsw05q/ (before.tar.gz plus before/protected manifests). Raw logs, demo credentials, databases, dumps and failure traces stay private.

## Results

| Check | Actual local result |
|---|---|
| Baseline | 80 frontend tests/lint/build; backend 125 discovered, 121 passed/four PostgreSQL-only skips |
| Module 1 | 13 focused authentication/closed-gate backend tests passed |
| Module 2 | 17 focused student tests passed |
| Module 3 | 24 focused ownership/visit tests passed |
| Module 4 | 30 focused planner/student tests passed |
| Modules 5–6 | 49 focused corpus/practice/ownership tests passed |
| Module 7 | 26 focused strict-Tutor/ownership tests passed before additional history regression |
| Frontend | 86 tests in 11 files passed; lint and production build passed |
| Complete backend | **185 discovered: SQLite 180 passed/five PostgreSQL-only skips; PostgreSQL 186 passed, no skips** |
| Student Chromium | Three complete tests passed at 1280/390px; registration/persistent sessions, owned learning, practice history, planner, cross-user denial, themes and automated WCAG 2/2.1 A/AA scans |
| Existing fixture Chromium | 15 tests passed; desktop/tablet/mobile shell/tree/theme/safety regressions |
| Source-copy migration | Fresh read-only backup copied original 0004→0012; all 18 original tables/437 rows/columns/IDs/counters preserved, integrity ok/FK0 |
| PostgreSQL transfer | Synthetic source incl. new student/planner/history: 39 tables/222 rows exact; deleted-ID counters and M2Ms preserved; one media file verified |
| Native PostgreSQL restore | Custom dump restored into a second NEW local target; 39 tables/37 sequences/FKs matched, records unchanged |

Existing integration: **9 passed** (Admin publication/review/withdrawal, dynamic popups/tags/collections, strict Tutor, PDF/CSP/accessibility). Academic sample Chromium: **4 passed**, query-only verifier checked 97 requests and five distinct 15-question subject pools. Final student run: **3 passed**, including logout clearing private reader state. Frontend: **86 passed**, lint/build passed. Independent SQLite spend race guard passed eight parallel contenders at the 4,000-micro ceiling. Django checks report no issues and no missing migrations. Protected data check: **28 original file hashes unchanged**, four original/demo databases integrity ok/FK0 and original migration files unchanged. Index remains empty and committed HEAD unchanged. The PostgreSQL runtime used here was private, disposable **16.2**, not an installed Homebrew service or production server. CI still targets 17; this task does not claim a new remote CI result. At base SHA, prior CI run 39632028522 failed test:e2e; local fixture rerun passed without weakening assertions. Current pipeline adds student tests but is not pushed.

## Reproduce isolated checks

Use pinned Node 24.22.0/Python 3.14.6/Django 6.0.9, hash-locked dependencies and synthetic/mocked data.

```sh
npm run check
backend/.venv/bin/python backend/run_tests.py
backend/.venv/bin/python backend/manage.py check --settings=core.test_settings
backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
backend/.venv/bin/python scripts/check_docs.py --release
backend/.venv/bin/python scripts/release_manifest.py
npm run test:e2e
```

Default backend tests use isolated SQLite. The PDF subprocess memory guard needs host process visibility; the sandbox-only baseline had one PDF-state failure, and the process-visible rerun passed without changing the guard. Use the host-visible approved runner rather than relaxing production bounds. Tests mock provider construction/network; no .env or real databases are read by the runner.

PostgreSQL: explicitly provision a disposable loopback base named prepal_test_*, set PREPAL_TEST_POSTGRES=1, POSTGRES_HOST/PORT/DB/USER/PASSWORD/SSLMODE and a NEW POSTGRES_TEST_DB named test_prepal_*, then `backend/.venv/bin/python backend/run_tests.py --postgres`. The guard refuses nonlocal/non-test names or an existing test DB. This role may need CREATEDB; production runtime roles must not. No command here approves production infrastructure or cutover.

Browser suites rebuild shared dist/output and must run **serially**. Use a new private PREPAL_DEMO_ROOT per mutable fixture suite:

```sh
# Prepare new synthetic PDF/Admin fixture with host process visibility.
PREPAL_DEMO_ROOT=/absolute/new/private/integration backend/.venv/bin/python scripts/prepare_demo.py
PREPAL_DEMO_ROOT=/absolute/new/private/integration npm run test:integration
# NEW destinations only; never reset or migrate the preserved demos.
backend/.venv/bin/python scripts/prepare_sample_demo.py --directory /absolute/new/private/sample
PREPAL_DEMO_ROOT=/absolute/new/private/sample backend/.venv/bin/python scripts/verify_sample_demo.py
PREPAL_DEMO_ROOT=/absolute/new/private/sample npm run test:sample
backend/.venv/bin/python scripts/prepare_student_demo.py --directory /absolute/new/private/student
PREPAL_DEMO_ROOT=/absolute/new/private/student npm run test:student
```

Local Chromium is viewport emulation, not physical-device/manual screen-reader certification. Axe scans are not comprehensive accessibility certification. Google signed-token exchange/state/nonce/collision/replay and recovery tokens/mail are tested with mocks/locmem, not live consent or delivery. Gemini scope/refusal/citations/quotas/timeout are mocked, not live factual or billing validation.

## Diagnosed verification failures

Historical migration regression originally queried current UserProgress/QuizAttempt classes while deliberately at schema 0007; corrected it to use MigrationExecutor historical models. Initial new browser locators used label text containing a hidden option letter; switched to accessible radio roles. Planner task state updates only after the server response; browser click then waits for the checked state. An overlapping failed browser restart caused trace-artifact errors; suites are subsequently serial. A partial integration demo seeded in the sandbox failed bounded PDF extraction, so it was preserved and a NEW host-visible fixture prepared. No original data or safety guard was modified to make tests pass.

The first expanded transfer fixture used the wrong StudyTask title field; corrected fixture to topic_title. The old rehearsal expected the content-only gate without explicitly selecting it; rehearsal now explicitly sets STUDENT_FEATURES_ENABLED=false before its containment smoke checks. Student-on behavior is independently covered by the full API/PG suites. No failures are silently omitted or marked skipped to obtain green results.

## Release/data integrity

Use `scripts/release_manifest.py --export` only with a NEW private directory outside the application. It hashes required source/config/migrations/tests/docs, checks ignore eligibility and rejects private artifacts/known local values. Fresh locked installs and checks must use the export without .env/databases/media. Run redacted Gitleaks plus independent exact-value checks; Gitleaks misses the known retired historical Django key. That key remains retired and no history rewrite is authorized. Existing protected hashes, SQLite query-only integrity/FKs and Git HEAD/index are rechecked before reporting.

## Final release verification

The private clean worktree export contains **236 hash-verified required inputs** and no private artifacts. Fresh `npm ci --offline` and hash-locked Python installation succeeded; export backend185 discovered/180 passed/five PostgreSQL-only skips. Final frontend86 tests/lint/build are verified after the reset flow refresh/navigation fix. Dependency versions/lockfiles are unchanged. Source and exported inputs are compared byte-for-byte after documentation synchronization; this is an uncommitted worktree export, not a clean committed checkout or deployment.

Release and seven reachable-commit history Gitleaks scans passed with full redaction. Independent exact checks found zero current/retired values in release inputs and zero five-current-private-value matches in reachable Git blobs. One already-known retired historical credential blob remains; it is absent from the current local environment. A parser exception in the first exact-scan attempt echoed that retired historical value in tool output; the scanner was corrected to inspect constants without emitting values. No active credential was exposed or written to source, and no history was rewritten. Private exact-secrets.json records counts only.

All28 protected hashes, original migrations, four query-only SQLite integrity/FK checks, empty index/unchanged HEAD, diff whitespace and Git fsck pass. Documentation destinations pass for19 canonical release documents. No new remote/CI claim. The temporary synthetic PostgreSQL cluster is stopped after verification; retain its private data/dump/manifests, never use this disposable runtime for production.
