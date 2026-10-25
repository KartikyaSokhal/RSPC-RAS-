# Recovery navigation race verification — 25October2026

The formerly failing assertion is deterministically reproduced as a permitted intermediate state: hold refreshStatus unresolved, observe exact reset-page status and no login heading; resolve that same promise in act, await the final login heading, then assert the original complete success text and refresh call. This proves correct navigation without altering application code. Twenty separate Vitest processes pass; no retries, timeouts added, sleeps, assertion removal or weakened checks.

Reproduce from application root under pinned Node24.22.0: node node_modules/vitest/vitest.mjs run src/test/student-platform.test.jsx -t 'clears the recovery fragment'. Twenty individual logs and repeated-test.json are private at ../.recovery/prepal-ci-navigation-4azshwe2/. Full npm run check passes90tests/13files, ESLint and production build. Both full backend suites rerun:224 PostgreSQL17 passes;219 SQLite passes/five PostgreSQL-only skips. Guarded PostgreSQL17.11 initializer/native encrypted independent recovery passes11 assertions and verifies40tables/1237rows/37sequences. Migration consistency no changes; Django system0issues. Runtime/development pip-audit zero, npm runtime audit zero and pip check clean. Protected17 hashes unchanged; no runtime/authentication, dependency, model, migration or hosted-data changes. Previous parent CI failure is retained below; new matching remote CI must be inspected after normal publication before acceptance.


Final local result: all33 Chromium journeys pass (15public,9integration,4sample,5student), plus20independent recovery-test runs and90frontend tests/lint/build.19 canonical documentation files/271 release inputs validate; exact five-file scope and preservation of all four pre-existing documentation updates verified. No source/history scanner findings; independent staged private-value checks are mandatory before commit. All17 protected hashes and other tracked runtime/config/model/migration/dependency files are unchanged. Publish normally only after staged checks and verify the exact new CI run; live initialization/deployment remain separate approval gates.

---

# Actual post-push CI failure — 25 October2026

25October2026 post-push result: commit6b29e39fc94d982309f307d64e7a6518d96b39e1 is normally pushed to main; remote SHA matches. [CI40169515420](https://github.com/KartikyaSokhal/RSPC-RAS-/actions/runs/40169515420), job121097333587, FAILED at npm run check:89frontend passed/one failed. Backend, PostgreSQL17 initializer and browser CI steps were skipped. Do not call this release CI-accepted or use prior CI as acceptance. No CI retry or follow-up code change was made after failure; owner stop gate applies.

Failure: src/test/student-platform.test.jsx:91, recovery-fragment/session-refresh test expected "Password changed. Sign in with your new password." but received intermediate "Password changed." ResetPasswordPage sets its status before awaiting refreshStatus and navigating; findByRole('status') can resolve against that intermediate element. Timing-race diagnosis is inferred from the exact log/code, not a proven product failure. These frontend files are byte-identical to the parent commit and were outside this28-file release; local90tests and33Chromium passed. Do not weaken assertions, blindly retry CI or change product authentication behavior.

Exact next task needs approval: narrowly update src/test/student-platform.test.jsx to await completed login navigation/final status before asserting the unchanged full success message and session-refresh call, run focused/full frontend checks and regressions, review the extra test-file diff, then commit/normal push and verify its own CI including PostgreSQL17. Until then stop publication/deployment/live initialization. The following pre-push local verification remains valid for its stated environment only.

---

# Patched PostgreSQL17 publication verification — 25 October2026

Exact28-file boundary: previously reviewed25 plus approved3 dependency files;271 pre-patch source inputs hash-archived outside checkout;17 protected database/media/environment hashes unchanged. PostgreSQL17.11 source SHA256 dd27f2b3c59e73ed14aa3324901242bf69a032a6347805f274e6260322d42979 verified against official ftp.postgresql.org. Built native server/pg_dump/pg_restore/psql17.11 with OpenSSL; private loopback SCRAM cluster only. No global install or hosted writes.

| Check | Actual result |
|---|---|
| Full backend, PostgreSQL17.11 |224 passed,0 skipped |
| Full backend, isolated SQLite |219 passed,5 PostgreSQL-only skips |
| Frontend |90 passed/13files; lint/build pass on Node24.22.0 |
| Chromium, fresh synthetic fixtures |15 public +9 integration +4 sample +5 student =33 passed |
| Django/migrations |System check0issues; makemigrations check no changes |
| PostgreSQL transfer/concurrency |Existing disposable transfer and budget-race checks passed |
| Guarded initialization and recovery |11 assertions pass;30 migrations, exact synthetic corpus, idempotence, unknown/nonempty refusal, advisory concurrency refusal, all-migration rollback, runtime denials and Admin/API gates |
| Native encrypted restore |AES256-GCM authenticated snapshot restored in NEW PG17 target in one transaction;40 tables/1237 rows/37 sequences match, including row/PK hashes; wrong recipient and tamper refused before extraction |
| Hosted connectivity/privileges |Both existing limited roles independently authenticate over verify-full; native psql17.11 confirms server17.11/TLS/read-only; target still empty, no live changes |
| Dependency security |PASS: pypdf6.21.2 installed with regenerated hashes; runtime and development pip-audit zero; pip check clean. Only pypdf pin/hashes change. npm runtime audit zero |
| Git/secret state |Approved publication from ff4acdc, normal push only; exact staged inputs/private-value checks required before commit. Known retired historical key remains retired |
| Remote CI |New release must pass its own Actions job including explicit PostgreSQL17 initializer rehearsal. Prior ff4acdc run40110060327 success is historical, not candidate acceptance |

Patched31focused PDF/content/Admin regressions pass. Private patch/source/log/rehearsal evidence: ../.recovery/prepal-pypdf-release-gu5_5t3f/. Native runtime/prior evidence: ../.recovery/prepal-pg17-publication-tz8_ejzs/. Previous16.2 results are historical and superseded for this initializer by actual17.11 evidence. First hosted metadata probe failed on the test harness accessor (info.ssl_in_use); corrected to pgconn.ssl_in_use and both-role/native checks passed without writes. No security assertion was disabled. Test recovery recipient/key is local0600 under0700, not durable off-host production custody. No live initialization or Render mutation. Approved pypdf6.21.2 remediation is now applied with no other dependency upgrades or advisory suppressions. Publication requires exact final checks and matching remote CI; local success does not establish hosted application acceptance.


Final source checks:19 release documents and271 inputs validate; clean private export installs hash-locked Python/npm dependencies, builds React and collects159 Admin/static files (459 post-processed) without database access. Gitleaks source/reachable-history scans and independent exact active/retired-value scans are clean; original SQLite/demo query-only integrity/FKs and17 protected hashes pass. CI YAML parses with postgres:17; new initializer CI remains unrun/unpublished. Final staging/commit/push is authorized only after exact checks; the resulting SHA/CI are reported after publication.


25October patched-source final rerun: all33 Chromium journeys pass (15public/9integration/4sample/5student). Clean private export installs the regenerated hash locks with pypdf6.21.2, builds React and collects159 static files/459 post-processed. Npm runtime audit zero, full runtime/development pip-audit zero;19 canonical docs/271 release inputs validate. PostgreSQL17 guarded initializer and authenticated encrypted independent restore passed again with the patched environment. No original data, migrations, hosted credentials or deployment changes. The approved publication SHA and its matching CI outcome must be checked after the push; no earlier CI result substitutes for it.

---

# Authenticated Render read-only audit — 24 October2026

Local and remote main ff4acdc442cb971bd1e609433bd7de28488ddab1 verified, clean preflight. Browser account/resources/current flags/start/build/auto-deploy and four historical deployments inspected without mutation. Existing ignored private connection file used directly; no credential output. Strong TLS connection passed against the exact external endpoint with verify-full/trusted certifi, PostgreSQL17.11/TLS1.3/TLS_AES_256_GCM_SHA384. Enforced startup default_transaction_read_only, explicit repeatable-read READ ONLY, verified transaction_read_only=on and rolled back. No migration, seed, DDL or data write.

Catalog/aggregate audit: only public non-system schema; zero non-system relation objects, routines or large objects; no django_migrations/auth_user; zero application rows/users/content. Five cluster login roles exist; current role is non-superuser/non-replication/non-BYPASSRLS but has CREATEDB/CREATEROLE. Private database-audit.json stores safe aggregate/privilege results only. Source graph inspected offline (no DB):30migrations, content0001–0012 plus framework18. Canonical corpus validates142topics/five roots/15lessons/15quizzes/75questions/300choices/19tags/15aliases/30curated relations/30published topics including ancestors; proposed single synthetic staff, zero students/uploads. These are planned initialization counts, not hosted data.

Evidence and verified pre-edit docs archive are private at ../.recovery/prepal-render-readonly-fecadz1d/. Existing root.env bytes and protected original/demo/media/environment hashes are preserved. Current batch edits documentation only; previous full application/CI results are historical, not rerun or hosted acceptance. Documentation/release/secret checks are run for these edits. Startup remains blocked by missing demo acknowledgement flags, empty schema/content, broad runtime role and network acceptance. No full app startup, provider call or live deployment was attempted. Final local checks:10focused free-demo tests passed;19release documents and264release inputs validated;Gitleaks0 and exact private Render credential matches0;17protected hashes unchanged;git diff --check clean. No new full-suite or hosted application claim.

---

# Free-demo publication verification — 24 October2026

Approved candidate264inputs matched the previous final manifest before edits; private recovery archive verified. Current main base038a4b2 contains approved1e685ee and has identical tree. Public repository visibility was verified in GitHub UI and explicitly approved by owner. Render auto-deploy was saved Off before push and rechecked after navigation; build unchanged, start deferred because live prerequisites fail. No live DB query/write or redeploy.

Rerun under pinned Node24.22.0:90frontend tests/13files;lint/build pass;15public Chromium pass. Full Django219discovered/214passed/five PG-only skips;system check0issues;makemigrations --check --dry-run nochanges. The first sandboxed full run and focused PDF regression failed because the existing macOS worker requires /bin/ps; unchanged full suite passed outside the sandbox in15.631seconds. No assertions or extraction code changed. Four private Gunicorn/free-demo journeys rerun against the existing isolated synthetic SQLite fixture only; no live provider. Staged manifest/diff/secret results are verified before committing and preserved privately. This task does not claim authenticated hosted PostgreSQL or successful hosted app acceptance. CI is verified for the actual published SHA after pushing, not inferred from prior green runs.

---

# Restricted free-demo verification — 24 October 2026

Baseline source SHA1e685ee2a7b408fe6936dd0245fa776630d3286e. New free-demo profile is local/uncommitted; no live environment/database edits, Git release or redeploy. Details and private evidence are in the top handoff and DEPLOYMENT.

Verified live read-only observations: designated account; existing Free web service and Available Free PostgreSQL17; database expiry23November2026; current settings/internal hostname/verify-full; last deployment failure at staging guard before DB access. A PostgreSQL SSLRequest probe against the external hostname verified the trusted certificate/hostname and TLS1.3. It sent no login credentials and executed no SQL. The browser's redacted connection string was detected as a placeholder and could not authenticate; that is not evidence of database authentication failure. Actual PostgreSQL SELECT1/schema/role/data and web-service-origin connectivity remain unverified pending a private environment file. Nothing was bypassed or written to the live database.

Automated backend adds10tests for explicit synthetic mode/strong settings, refusal of lower TLS or internal host, trusted CA, immutable production boundaries, learner closures for guests/staff, provider non-invocation, staging barrier, read-only Admin, rejected multipart/direct-storage writes, safe health and route/static behavior. Full suite219discovered:214passed/five PostgreSQL-only skips on final rerun. First full run hit the existing quiz equality test across a signing-timestamp second; only revision-token bytes differed. No quiz code/assertions were changed; full rerun passed. Original method-boundary test now posts explicit JSON so it checks405, while the free-demo tests separately assert403 for multipart before parsing.

Local actual Gunicorn+Chromium smoke uses a NEW marked15lesson/75MCQ synthetic SQLite fixture, not active8002 or original demos. Four journeys passed: Basic barrier/public health; React/closed flags/Admin assets; published notes/approved popup/390px and1280px automated accessibility/themes; closed learner operations/Admin writes/uploads/private paths. Synthetic content/account/learner counts unchanged; Django deploy check passes. This tests the new runtime routing/static/middleware with the built React distribution. Local HTTP uses a test forwarded-HTTPS header to emulate TLS termination; it is not hosted HTTPS or a PostgreSQL-auth test. Initial browser attempt corrected only the Admin Username: label selector; no product guard was weakened.

Frontend lint/90tests/build pass. The host default Node26was detected, so a private vendor-SHA256-verified Node24.22.0 runtime is used for final pinned frontend/browser checks; no global/runtime project pin changed. Final source/release/secret/protected-data verification results follow in the task report/private receipts. No new remote CI run is claimed. Existing baseline CI39968769235 was green, including PG17; this new uncommitted profile was not run remotely.

Reproduction: use backend/run_tests.py and npm run check under pinned Node24; new backend free-demo tests are part of normal discovery. Private browser verification source/run result is in /Users/kartikyasokhal/Downloads/MYPLACE/rpsc/.recovery/prepal-free-demo-zqihtnby. Never point browser/test settings at hosted credentials or valuable data. Start/stop only loopback verification processes you created. Free-tier hosted acceptance remains gated on separate approval.

## Final local results for this candidate

| Check | Actual result |
|---|---|
| Full Django |219 discovered;214 passed;5PostgreSQL-only skips; final full rerun15.360s |
| Frontend under Node24.22.0 |90tests/13files, lint and production build passed |
| Existing public Chromium under Node24 |15passed,35.5s |
| Free-demo actual Gunicorn/Chromium under Node24 |4smoke journeys passed;zero failures |
| System/deploy/migration checks |No issues;no changes detected |
| Release and documentation |264release inputs;19release Markdown docs validate |
| Gitleaks |Zero findings in the release export |
| Protected data/config |16private hashes unchanged; production/staging/shared TLS/models/migrations/locks byte-identical |
| Live database TLS |External PostgreSQL SSLRequest certificate+hostname verified;TLS1.3;no login/SQL |
| Hosted web health |One HTTPS request timed out after12seconds;hosted app health unverified |
| Live SQL/schema/accounts |Not executed: browser credentials are redacted; no complete local shell connection config |
| Git/live state |HEAD1e685ee unchanged;index empty;no commit/push/redeploy/resource/env/DB write |

A12second timeout can reflect free-tier startup delay and does not prove a permanent outage. No security constraint was relaxed. The source profile is ready for owner review; authenticated read-only DB/schema/synthetic-data acceptance and any live configuration/initialization/redeploy remain separate steps.

---

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
