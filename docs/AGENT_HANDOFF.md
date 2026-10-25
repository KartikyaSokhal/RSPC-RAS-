## Current handoff — public-homepage Git publication, live activation gated

**Authority:** Owner approves verified normal commit/push of this reviewed candidate to main and exact matching fully green CI. No live DB writes/grants/account insertion, Render configuration changes, manual deployment, paid resources, real registration, OAuth/Gemini activation or valuable-data cutover in this batch. Preserve Auto-Deploy Off. Earlier authority/status entries below are history.

**Repository/release identity:** Baseline main/remote d2f014c186acba1360e9438a2382d13b85e74c6a, zero divergence at initial fetch. All42 existing changes (including19 canonical docs and the local student UI) were preserved in a verified280-input private archive. This release includes that work plus the hosted synthetic-only profile/operator/test additions. Resolve its actual code commit with `git log -1 --format=%H -- deploy/render-public-demo-start.sh`; confirm `git ls-remote origin refs/heads/main` and matching Actions. Exact SHA/run/result and remote equality are recorded after publication in parent `.recovery/prepal-public-publication-b5yplbn3/publication.json` and the final task report; do not assume prior baseline CI accepts new source. This handoff does not predeclare publication/CI success before the checks.

**Files in the reviewed candidate:**

- `.github/workflows/checks.yml`
- `AGENTS.md`
- `README.md`
- `backend/.env.example`
- `backend/README.md`
- `backend/content/management/commands/check_public_demo.py`
- `backend/content/management/commands/initialize_free_demo.py`
- `backend/content/management/commands/prepare_public_demo_login.py`
- `backend/content/services/public_demo_database.py`
- `backend/content/services/sample_content.py`
- `backend/content/student_auth.py`
- `backend/content/test_public_demo.py`
- `backend/content/test_render_public_demo.py`
- `backend/content/views.py`
- `backend/core/public_demo_settings.py`
- `backend/core/public_demo_support.py`
- `backend/core/render_public_demo_settings.py`
- `deploy/render-public-demo-start.sh`
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
- `e2e-public-demo/access.spec.js`
- `eslint.config.js`
- `package.json`
- `playwright.public-demo.config.js`
- `scripts/free_demo_database.py`
- `scripts/prepare_public_demo.py`
- `scripts/release_manifest.py`
- `scripts/verify_free_demo_database.py`
- `src/App.jsx`
- `src/api/client.js`
- `src/components/auth/LearningRoute.jsx`
- `src/components/auth/returnLocation.js`
- `src/components/layout/AppShell.jsx`
- `src/context/AuthContext.jsx`
- `src/pages/home.jsx`
- `src/pages/loginPage.jsx`
- `src/pages/resetPasswordPage.jsx`
- `src/pages/signupPage.jsx`
- `src/test/public-demo.test.jsx`

**Architecture/control:** Existing React/Django/PostgreSQL/session/StudentIdentity stack. Local core.public_demo_settings still refuses Render and is synthetic-loopback only. New core.render_public_demo_settings selects only exact existing hosted external DB/runtime role/5432, verify-full/trusted CA and exact HTTPS origin. No Basic middleware. Public homepage/login/signup shells and aggregate config/session endpoints; other APIs/React learning routes require student session. Hosted eligibility is the single active nonstaff privately generated example.invalid identity, not arbitrary student accounts. One-hour secure HttpOnly/Lax host-only cookies, CSRF/throttling/password hashing; original-route return and expiry/stale-status protections retained. Registration/recovery/Google/Gemini/uploads/Admin mutations stay closed; staff Admin authorization remains independent. Old private/production/staging/free-demo profiles and secrets are preserved.

**Known database and proposed transition:** Read-only authenticated hosted check verified the known corpus (142 topics/15 lessons/15 quizzes/75 questions/300 choices/30 migrations/one view-only staff/zero students/uploads), changed=false. New private random login identifier/password JSON is prepared0600 beside existing protected operator files, never displayed or inserted live. Do not publish credentials, copy operator env to Render, reset/reseed the nonempty DB or run migrations. The approval-gated student-login operator transaction creates exactly one synthetic User/StudentIdentity, extends the existing marker JSON with public_demo.version/student_id/username and grants fixed owned-table/sequence/UPDATE(id) row-lock privileges. It refuses unknown/valuable/ownerless data, unsafe roles and password mismatch; repeats verify without reset. Existing initializer default remains zero-student and refuses the extended state. No new schema/migration. Runtime has no DDL/admin/ownership/membership; UPDATE(id) technically permits ID edits and is not a final production role policy. Failed transactions may leave harmless sequence gaps, never resets. Bounded read-only startup checks refuse unexpected marker/schema/migrations/counts/identities/privileges before Gunicorn binds; full corpus checks remain operator-only.

**Tests/evidence:**111 frontend tests/lint/build;240 PG17.11 backend passes;235 SQLite passes+5 PG-only skips;36 Chromium passes on fresh fixtures;16 native17 initializer/controlled-login/recovery assertions, including40-table/1237-row/37-sequence independent encrypted restore; real restricted runtime post-use corpus/ownership/privilege checks; bash/pip/schema checks. TESTING records initial resolved fixture/verifier issues and limits. No real provider requests or hosted acceptance/deployment of this candidate. Entry archive, current release/staged/secret logs, protected hashes, local test fixtures/operator plans and actual publication receipt are private at parent `.recovery/prepal-public-publication-b5yplbn3/`. Protected original databases/media/environment files remain unchanged. Final security/source/export checks must be complete before commit, and GitHub CI must be fully green for its exact SHA before reporting release success.

**Existing Render state:** Designated account kartikyasokhal28@gmail.com / My Workspace / Prepal / Staging, existing Free RSPC-RAS- service srv-dbe6d5vb9u1s738ikh80 and prepal-staging-db only. UI shows main, deployed d2f014c, build bash deploy/render-build.sh, start bash deploy/render-free-demo-start.sh, health/api/health/ and Auto-Deploy visually Off. No Edit/Save/Manual Deploy or secret reveal/copy action was performed. Current private barrier, actual runtime/service secrets and TLS remain in place; the previously retired Django key stays retired. Original operator barrier/signing values are not replacement Render secrets.

**Exact next task:** After verified Git publication/green CI, owner reviews/approves [the live packet](DEPLOYMENT.md#hosted-public-homepage-demo-approval-packet): fresh read-only native encrypted snapshot and exact synthetic/role/TLS preflight, additive student-login --apply/limited grants, runtime verification, then Save-only specified Render profile/start variables. Do not execute them based on Git approval. Afterwards request explicit manual deployment authority and select the exact green-CI SHA. Hosted acceptance must use a fresh browser without cached Basic credentials; verify public home/auth pages, protected APIs/routes/original redirect, private synthetic login/owned writes/logout, Admin/static/health/HTTPS/CSRF/mobile/a11y and closed providers/signup/uploads. No real student data. Durable nonexpiring PostgreSQL, independent off-device recovery custody/scheduled backups/retention/restore/RPO-RTO, operations, public-auth/staff/abuse/privacy/deletion/media and production role-policy acceptance remain real-registration blockers. The existing disposable-only recovery waiver never covers real students.

Final local release checks:286 release inputs/19 canonical documents validate; protected17 file hashes and original migrations/private production profiles unchanged; npm/pip runtime advisories0, pip check clean, budget concurrency ceiling check passed. Hosted login identifier/password are both privately generated in0600 JSON outside Git and are absent from source; no live account exists yet. Source/staged secret scans, export checks and exact publication/CI receipt are required gates; publication receipt is written only after actual remote verification.

---

## Current handoff — LOCAL student-gated public preview, 25 October 2026

**Authority/state:** Main/HEAD remains `d2f014c186acba1360e9438a2382d13b85e74c6a`. No commit, staging, push, Render change, hosted migration or deployment in this task. The earlier14 modified documentation files were present at entry, privately archived with all271 then-current release inputs and preserved verbatim beneath current additions. This local student preview supersedes old task instructions only for its approved scope. Existing deployed restricted free-demo remains unchanged, with Basic protection, Auto-Deploy Off, verify-full and closed student/AI services. Do not mistake previous hosted acceptance for this new profile's deployment.

**Implementation:** New core.public_demo_settings is explicitly local/marked/PostgreSQL-only and refuses Render/production/hosted/SQLite targets. It reuses existing Django sessions, StudentIdentity and owned services. Public homepage and login/signup pages issue no Basic challenge; signup is informational and registration/recovery remain server-disabled. Only counts/feature policy/CSRF/health/session endpoints are public; all other APIs fail closed for active nonstaff student identity, with no Basic credentials accepted. LearningRoute guards existing learning pages; AppShell does not fetch hierarchy for guests; login returns to validated local path/query/hash. Expiry clears private UI, and versioned status refresh prevents a stale response undoing logout. Django Admin remains staff-authorized/read-only; uploads, Google and Gemini are disabled. No new authentication backend or schema.

**Source/test/config files changed or added in this task:**

- `.github/workflows/checks.yml`
- `backend/content/student_auth.py`
- `backend/content/test_public_demo.py`
- `backend/content/views.py`
- `backend/core/public_demo_settings.py`
- `backend/core/public_demo_support.py`
- `e2e-public-demo/access.spec.js`
- `eslint.config.js`
- `package.json`
- `playwright.public-demo.config.js`
- `scripts/prepare_public_demo.py`
- `scripts/release_manifest.py`
- `src/App.jsx`
- `src/api/client.js`
- `src/components/auth/LearningRoute.jsx`
- `src/components/auth/returnLocation.js`
- `src/components/layout/AppShell.jsx`
- `src/context/AuthContext.jsx`
- `src/pages/home.jsx`
- `src/pages/loginPage.jsx`
- `src/pages/resetPasswordPage.jsx`
- `src/pages/signupPage.jsx`
- `src/test/public-demo.test.jsx`

**Documentation:** All19 existing canonical documents now describe this profile or its relevant state/API/Admin/security/test/continuation consequences. No duplicate handoff/report was created. The complete old deployment evidence and significant decisions remain in place below. Review the exact worktree diff; do not discard prior documentation edits.

**Database/migrations:** No new migrations/models. Existing30 migrations (content0001–0012 plus18 framework) applied to NEW disposable local PG17.11 `prepal_local_public_demo_auth_20261025` on loopback61348. Corpus:142 topics,15 published synthetic lessons,15 demo-reviewed quizzes,75 questions,300 choices, one view-only staff and two synthetic StudentIdentity accounts, zero real students/uploads. Browser tests added only synthetic owned records. Original SQLite, existing demos/media and hosted database untouched;17 protected hashes verified unchanged. Native17 test cluster is private, separate from hosted Render. Migration/runtime secrets and generated account passwords are outside application Git at parent `.recovery/prepal-public-demo-_3up9ot_/{migration.env,runtime.env,demo/accounts.json}`, permissions0600; never print/publish them.

**Runtime policy/limitation:** No DDL/database CREATE/TEMP/ownership/admin flags/membership. Session/auth bookkeeping plus owned learner tables/association tables are writable. Canonical educational fields are read-only. Existing SELECT FOR UPDATE grading requires UPDATE privilege; local role has UPDATE(id) only on Question/Choice/Quiz/QuizReview/TopicPublication. This technically permits ID mutation, so do not claim SQL-level immutability; review locking/role design before production. The hosted read-only role was never changed. The new preparer refused its populated target before writes, verified by all-table hashes. No reset/adoption behavior.

**Verified:**111 frontend tests, ESLint/build;234 PG17 backend passes;229 SQLite passes +5 PG-only skips;36 Chromium passes (15 public/9 integration/4 sample/5 student/3 new PG public-preview); local Django/system/migration consistency; no new migration files; npm/pip runtime advisories0. Details and initial resolved test/config/grant issues are in TESTING. Mac sandbox /bin/ps denial causes the existing bounded PDF regression to fail; full tests passed with required process-monitor access, without changing parser limits. Public browser tests use loopback HTTP; no hosted HTTPS/cookies/public enrollment acceptance is claimed. New CI wiring is unpushed/unexecuted on GitHub.

**Final release verification:**280 release inputs/19 canonical docs validated; gitleaks0; fresh generated runtime/signing/account values absent from source; no staged files or tracked private environment/database/key artifacts; git diff --check and pip check passed. Clean private source export installed with offline npm ci and passed111 tests/lint/build. Source recovery archive and final release export are under parent `.recovery/prepal-public-demo-_3up9ot_`. PostgreSQL test cluster was stopped after verification; databases/roles/configs/corpus are preserved. For another local review, start the existing private cluster at `.recovery/prepal-pg17-publication-tz8_ejzs/cluster17` using its native17 pg_ctl, then load only the new local runtime.env and follow DEPLOYMENT. No hosted target was contacted. Working changes total42 files (19 canonical docs +23 source/config/test files); all14 prior modified docs remain intact. This has not been published or accepted as production authentication.

**Remaining blockers / exact next task:** Owner reviews this local diff, documented runtime column-grant limitation and synthetic results. Do not deploy this local-only settings module or remove the live barrier. Before a hosted student profile is designed/activated, obtain approval for a nonexpiring persistent database, separated roles/TLS, encrypted scheduled backups/retention and independent off-host recovery-key custody + tested restore/RPO/RTO, same-origin HTTPS/secure cookies/CSRF/proxy/static/private-storage controls, staff security, registration/email verification/abuse/reset/enumeration/retention/deletion/privacy operations, content rights and monitoring. The disposable-demo loss waiver never covers students. Git publication, environment activation and deployment each need separate authority. Keep Google/Gemini and uploads off. See [DEPLOYMENT](DEPLOYMENT.md#local-student-gated-public-preview), [SECURITY](SECURITY.md) and [TESTING](TESTING.md).

---

# Current handoff — live restricted synthetic demo

25 October 2026: the existing restricted demo is LIVE at https://rspc-ras.onrender.com. Render deployment dep-dbevgpfavr4c73c9m9i0 succeeded for main commit d2f014c186acba1360e9438a2382d13b85e74c6a at 18:11 IST. Matching GitHub Actions40171764725 is green. Account kartikyasokhal28@gmail.com / My Workspace / Prepal / Staging; existing Free web srv-dbe6d5vb9u1s738ikh80 and existing PostgreSQL dpg-dbe7a1oae00c73c5g090-a only. No new resource, purchase, upgrade, production release or valuable-data cutover.

Branch main/HEAD remains d2f014c186acba1360e9438a2382d13b85e74c6a. Only the following documentation files changed locally; no code/model/migration/dependency edits, staging/commit/push or new GitHub CI run. The six pre-existing documentation changes were preserved in a hash-verified271-input private pre-edit archive.

- AGENTS.md
- README.md
- backend/README.md
- docs/AGENT_HANDOFF.md
- docs/DEPLOYMENT.md
- docs/PROJECT_STATUS.md
- docs/SECURITY.md
- docs/TESTING.md
- docs/FEATURES.md
- docs/CHANGELOG.md
- docs/MVP_SCOPE.md
- docs/IMPLEMENTATION_PLAN.md
- docs/DECISIONS.md
- docs/DATABASE_SCHEMA.md

PREPAL_ENVIRONMENT=free-demo, PREPAL_FREE_DEMO=1 and PREPAL_FREE_DEMO_SYNTHETIC_DATA=1; external PostgreSQL host dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com with POSTGRES_SSLMODE=verify-full and trusted CA. Build bash deploy/render-build.sh; start bash deploy/render-free-demo-start.sh; health /api/health/; Auto-Deploy Off. Production security profiles are unchanged. Student authentication/progress/planner/attempt saving, Google, Gemini/email, uploads and Admin content mutations remain disabled; the private staging barrier remains required.

Exactly30 migrations applied (content0001–0012 plus18 framework migrations),142 original syllabus topics/five subjects,15 sample note lessons,15 quizzes,75 questions,300 choices,19 tags,15 aliases,30 publications including ancestors,30 curated relationships and30 approved links. Exactly one synthetic view-only staff sample-editor, zero students/uploads/bookmarks/progress/saved attempts/AI requests. Engineering sample notices and quiz review reasons are not human academic approval.

Guarded initialize, reviewed grant-runtime and runtime verify succeeded. Post-browser read-only runtime verify passed again with changed=false and all counts unchanged. Actual runtime probes reject DDL, content UPDATE and sequence SELECT with42501; all probes rolled back. Runtime has content/framework SELECT, session CRUD and auth_user last_login/password bookkeeping only; no schema/database CREATE/TEMP, object ownership, privileged role flags or memberships. Server/native client17.11; TLS1.3/AES256GCM with verify-full. Existing SQLite/media/environment hashes are checked separately; no valuable source was transferred.

Actual hosted Chrome checks passed: homepage142/five counts,142-link full expansion/five-root collapse, light/dark toggle, all15 sample lessons and their approved links/tags/related content, popup focus/new-tab attributes/Escape/focus restoration, three tag pages with exact counts, Monsoon search, all five subject practice pools and75/75 correct stateless scores, synthetic Admin login/session persistence/view-only detail/logout and five loaded Admin stylesheets. Config reports demo=true and student/AI/Google=false. Learner API error codes verified for guests and logged-in staff; Tutor request rejected as unavailable before provider work. HTTPS health200/status ok; unauthenticated homepage/config/Admin401 with Basic challenge, private/no-store/noindex; HSTS/nosniff/frame DENY verified. Keyboard skip-to-main, one main/one h1, no unnamed buttons and no horizontal overflow passed at1512px. This is a desktop browser smoke check, not a fresh mobile/axe/screen-reader/load audit.

Fresh local security/initializer guards:15passed, system check0issues. Previous-turn same-source frontend90tests/lint/build pass; matching-source remote CI includes PostgreSQL17/backend/browser checks. No new full local backend/mobile/axe suite was claimed for documentation/hosting-only work. Docs/release/secret/protected-hash final results are in ../.recovery/prepal-live-deploy-xjhhgl_i/final-integrity.json.

Security incident and resolution: Render Copy value unexpectedly populated the staging password in browser accessibility output. It was not copied into source, documentation or evidence files. Owner confirmed replacing ONLY STAGING_ACCESS_PASSWORD with a new strong value using Save only; that replacement was not retrieved or displayed. Owner then completed native Chrome Basic sign-in and actual hosted tests succeeded. Do not reuse the exposed barrier value. Never use Render Copy/reveal controls for credentials in future automation; preserve passwords/signing keys, suppress secret-bearing AX field values and prefer owner native sign-in. No DB credential, recovery key/passphrase or Django signing key was exposed in this incident; the separately known historical Django key remains retired.

Owner explicitly waived permanent independent/off-device recovery-key custody ONLY for this disposable synthetic database; durable custody remains unconfirmed and production safeguards are not waived. A real read-only native pg_dump17.11 CMS AES256GCM snapshot now contains40tables/1237rows/zero uploads, encrypted to the dedicated owner certificate. Private snapshot/receipt are in ../.recovery/prepal-live-deploy-xjhhgl_i/hosted-encrypted-backup/. The dedicated key/restore tooling passed the earlier independent LOCAL PostgreSQL17 restore; this hosted snapshot was not restored live. No daily scheduler, off-host retention or production30-day guarantee is configured. Free cold starts/expiring DB remain unsuitable for valuable data.

Private current evidence: ../.recovery/prepal-live-deploy-xjhhgl_i/; initializer/runtime/post-browser logs, runtime-permissions.json, hosted-browser-checks.json, hosted-unauthenticated.json, hosted-security-headers.json, render-final-settings.json and real hosted screenshots. Staff password/operator role configs remain0600 in ../.recovery/prepal-demo-init-hw0bq8ne/render-roles/; do not bulk-copy operator SECRET_KEY/STAGING_ACCESS_* to Render or print credentials.

Exact next task: owner reviews the restricted live demo. Before any new implementation, obtain separate scope approval. Known presentation limitation: existing homepage/banner/reader copy still mentions AI capability or “Verified study notes” although this demo forces AI off and notes explicitly require human review; do not interpret generic UI labels as academic approval. A separately approved demo-copy follow-up would touch src/components/layout/AppShell.jsx, src/pages/home.jsx, src/pages/topicPage.jsx and src/components/ai/TutorPanel.jsx. Do not start Phase5, enable learners/AI, change production secrets, introduce uploads, buy services or transfer valuable data automatically.

Historical sections below document prior gates/results; they do not override this completed scoped deployment or production restrictions.

---

# Current handoff — owner recovery key verified locally; off-device custody pending

25October2026. Branch main/HEAD d2f014c186acba1360e9438a2382d13b85e74c6a unchanged; its CI40171764725 is green. This setup changes six existing documentation files only, uncommitted. No application/model/migration/dependency changes, Git publication, live initialization or Render mutation. Initial authenticated READ ONLY preflight verified exact prepal_staging_db/external host, server17.11, verify-full/TLS1.3, empty application schema and both restricted roles; native17 clients and operator0600/0700 permissions passed. No live migrations/rows/grants were applied. Offline graph remains30migrations through content0012.

Owner explicitly rejected one-day rehearsal recipients and authorized a new dedicated owner key. Public certificate: /Users/kartikyasokhal/Prepal-Recovery/free-demo-2026-10-25/public/prepal-free-demo-recipient.pem

SHA256 fingerprint: F8:FE:A1:03:BA:79:1E:72:A0:A7:5F:71:08:9E:01:4F:1C:2D:02:78:3E:EC:0B:DF:D1:32:68:8F:01:0F:E5:D4

Certificate valid25October2026–22October2036. RSA4096 private key is passphrase-encrypted PKCS8 PBES2/AES256CBC with PBKDF2-HMAC-SHA256600000 iterations, outside Git/Render/database server; no plaintext private-key file created. Owner-only directories0700/files0600 verified. The transfer TAR contains an already encrypted private-key copy and public certificate/recovery instructions; the TAR container itself is not encrypted. Passphrase/database credentials are excluded and the passphrase must be stored separately.

Real same-machine recovery test used the encrypted key extracted from the transfer kit, not the original key file: approved CMS AES256GCM backup decrypted and restored into a NEW local PostgreSQL17.11 database;40tables/1237rows/37sequences,142topics/15lessons/15quizzes/75questions/300choices/30migrations/one synthetic staff/zero students/uploads verified. Wrong passphrase and tampered CMS rejected; existing project archive/hash validation retained. Stock restore tooling lacks passphrase-file injection, so a private thin OpenSSL adapter supplies -passin file for CMS decrypt only; no application crypto code/TLS policy changed. Private local evidence remains in ../.recovery/prepal-live-init-preflight-gkz5o6ky/.

DURABLE CUSTODY IS NOT COMPLETE. Exact next manual task: owner stores the encrypted-key transfer kit off this Mac in an encrypted password manager or encrypted external drive, stores the passphrase separately in independently recoverable protected custody, retrieves/verifies the package checksum, and confirms both exist. Never request/paste private key or passphrase into chat/docs. After owner confirmation, reverify the recipient/custody and all target prerequisites before any resumed, specifically approved guarded initialize/grant-runtime/verify operation. The owner's latest instruction is no live initialization yet. Later Render credentials/demo flags/manual deployment require separate approval.

---

# Current handoff — approved recovery-test synchronization

25October2026. Branch main, base commit6b29e39fc94d982309f307d64e7a6518d96b39e1. Exactly five changed files: src/test/student-platform.test.jsx, AGENTS.md, docs/AGENT_HANDOFF.md, docs/PROJECT_STATUS.md and docs/TESTING.md. Four pre-existing failed-CI documentation updates are included and retained below. Private verified271-input pre-edit archive/evidence: ../.recovery/prepal-ci-navigation-4azshwe2/. Resolve this follow-up commit with git log -1 --format=%H -- src/test/student-platform.test.jsx; verify origin/main equality and the matching Actions run. Its actual SHA/run/outcome are recorded after push in that private directory's publication.json and the task report; no predeclared CI success.

Cause confirmed by controlled promise: ResetPasswordPage exposes its response status while awaiting refreshStatus, then navigates to LoginPage when refresh resolves. The old findByRole(status) could return the intermediate element and assert the destination message too early. With refresh deliberately pending the test verifies exact intermediate text, one refresh call and absence of login; after explicitly resolving refresh within act it asynchronously waits for the login heading and verifies the original full message and one refresh call. Actual authentication/router components are unchanged; no sleep/retry/assertion removal or coverage reduction. Twenty independent affected-test invocations passed.

Local checks:90frontend tests/lint/build,224 PostgreSQL17.11 backend tests,219 SQLite passes/five PostgreSQL-only skips, system/migration consistency, runtime/development pip-audit zero, pip check clean, npm runtime audit zero. Guarded initializer/native encrypted independent-restore rehearsal rerun passes all11 assertions, including unknown/nonempty refusal/rollback and runtime denials;40 tables/1237rows/37sequences recovered. Browser final results and source/staged checks are recorded in TESTING before publication. Original17 protected hashes, runtime/authentication/models/migrations/dependency locks and all existing data remain unchanged. The source still ends at content0012/30 total Django migrations; none applied live.

Native17 runtime and earlier read-only hosted compatibility evidence remain in ../.recovery/prepal-pg17-publication-tz8_ejzs/. Hosted operator files remain private at ../.recovery/prepal-demo-init-hw0bq8ne/render-roles/; do not rotate them or substitute their operator signing/barrier values into Render. No hosted SQL/settings/credential/demo-flag changes. Existing designated Render service main/build/start confirmed, Auto-Deploy visually Off; no redeploy or paid resources. Long-lived owner-controlled recovery recipient and separate durable/off-host private-key custody remain a live-initialization gate.

After matching fully green CI (including PostgreSQL17 initializer/transfer/backend jobs), exact next task is explicit guarded live-initialization approval: recheck empty exact target/identity/TLS/roles/network/private inputs and recovery custody, then execute only approved DEPLOYMENT initialize/grant-runtime/verify commands. Subsequent Render runtime credentials/demo acknowledgements and manual deployment need separate approval. Do not initialize, set flags, deploy or purchase from this test-fix authorization. The failed40169515420 run below describes the parent commit, not acceptance of this fix.


Final local result: all33 Chromium journeys pass (15public,9integration,4sample,5student), plus20independent recovery-test runs and90frontend tests/lint/build.19 canonical documentation files/271 release inputs validate; exact five-file scope and preservation of all four pre-existing documentation updates verified. No source/history scanner findings; independent staged private-value checks are mandatory before commit. All17 protected hashes and other tracked runtime/config/model/migration/dependency files are unchanged. Publish normally only after staged checks and verify the exact new CI run; live initialization/deployment remain separate approval gates.

---

# Current handoff — published commit; CI failure requires review

25October2026 post-push result: commit6b29e39fc94d982309f307d64e7a6518d96b39e1 is normally pushed to main; remote SHA matches. [CI40169515420](https://github.com/KartikyaSokhal/RSPC-RAS-/actions/runs/40169515420), job121097333587, FAILED at npm run check:89frontend passed/one failed. Backend, PostgreSQL17 initializer and browser CI steps were skipped. Do not call this release CI-accepted or use prior CI as acceptance. No CI retry or follow-up code change was made after failure; owner stop gate applies.

Failure: src/test/student-platform.test.jsx:91, recovery-fragment/session-refresh test expected "Password changed. Sign in with your new password." but received intermediate "Password changed." ResetPasswordPage sets its status before awaiting refreshStatus and navigating; findByRole('status') can resolve against that intermediate element. Timing-race diagnosis is inferred from the exact log/code, not a proven product failure. These frontend files are byte-identical to the parent commit and were outside this28-file release; local90tests and33Chromium passed. Do not weaken assertions, blindly retry CI or change product authentication behavior.

Exact next task needs approval: narrowly update src/test/student-platform.test.jsx to await completed login navigation/final status before asserting the unchanged full success message and session-refresh call, run focused/full frontend checks and regressions, review the extra test-file diff, then commit/normal push and verify its own CI including PostgreSQL17. Until then stop publication/deployment/live initialization. The following pre-push local verification remains valid for its stated environment only.

---

# Current handoff — approved pypdf security patch and PostgreSQL17 release

25 October2026. Branch main; publication base ff4acdc442cb971bd1e609433bd7de28488ddab1. Owner approves the existing25-file initializer candidate plus exactly3 dependency files, normal commit/push and matching GitHub CI verification. Resolve the candidate release SHA with git log -1 --format=%H -- backend/requirements.in; confirm equality with origin/main and inspect that exact SHA in Actions before live work. This handoff is part of the release commit and does not predeclare its future CI result; publication SHA/run/results are reported after push and preserved privately. No force-push, live initialization, Render change, deployment or purchase.

Verified271-input pre-patch recovery archive and new evidence: ../.recovery/prepal-pypdf-release-gu5_5t3f/. Prior native17 evidence remains ../.recovery/prepal-pg17-publication-tz8_ejzs/. Exactly28 approved changed paths; all pre-existing work and eight earlier audit document bodies retained. Only pypdf changes in generated locks:6.21.1→6.21.2 and its two package hashes; all other direct/transitive pins unchanged. Runtime and development pip-audit now report zero known vulnerabilities, pip check passes, no advisories suppressed. No application behavior/security policy/model/migration/production setting change for the patch.

Patched-dependency verification:31 focused PDF/content/Admin regressions;224/224 PostgreSQL17 backend;219 SQLite passes/five PostgreSQL-only skips;90frontend tests/lint/build. NEW local PostgreSQL17.11 guarded-initializer rehearsal passes all11 assertions: exact142topics/15lessons/75questions/300choices/one view-only staff/zero students/uploads,30 migrations, idempotence, unknown/nonempty refusal, advisory locking, rollback of migration DDL/content on injected failure, runtime42501 denials, CSRF Admin/API/gates, encrypted independent transactional restore40tables/1237rows/37sequences, wrong-key/tamper refusal and private key permissions. Existing disposable transfer and budget-race checks pass. Browser and clean-export final results are recorded in TESTING before publication. Remote CI must cover the initializer using the existing postgres:17 disposable service; encrypted native recovery is separately verified locally.

Native PostgreSQL server/pg_dump/pg_restore/psql17.11 are private at ../.recovery/prepal-pg17-publication-tz8_ejzs/tools/postgres-17.11/bin/, built from checksum-verified official source with OpenSSL. Previous24October read-only hosted evidence verified server17.11, verify-full/native psql TLS for both limited roles and empty prepal_staging_db. Neither role has unsafe administrative flags/memberships/database CREATE/TEMP; migration alone has public CREATE. No hosted SQL or credential/environment/network change is part of this patch. Existing designated Render account/service main/build/start rechecked; Auto-Deploy visually Off before push. No redeploy is authorized.

Prepared hosted operator files remain ../.recovery/prepal-demo-init-hw0bq8ne/render-roles/ (migration.env,runtime.env,staff-password.txt,plan.json),0600 under0700. Do not regenerate/rotate them or bulk-copy operator signing/barrier values to Render. Recipient test key is local0600 under0700 and excluded from Git; not approved durable/off-host recovery custody. Select an owner-controlled long-lived recipient certificate and secure the private key separately/off-host before live initialization. No backup scheduler, off-host copy or production30-day guarantee enabled.

Exact next task after matching successful publication CI: obtain explicit approval for the DEPLOYMENT initialize/grant-runtime/verify commands, first rechecking empty target/identity/roles/TLS/network/private credentials and recovery key custody. Then separately obtain Render runtime credential/demo-acknowledgement and manual-deployment approval. No valuable data, SQLite transfer, real students/uploads, paid AI or additional resources. Known retired Django key remains historical and retired; no history rewrite.

Files changed (includes the preserved prior audit documentation edits):
- `.github/workflows/checks.yml`
- `AGENTS.md`
- `README.md`
- `backend/README.md`
- `backend/content/management/commands/create_sample_content.py`
- `backend/content/management/commands/initialize_free_demo.py`
- `backend/content/services/free_demo_database.py`
- `backend/content/services/sample_install.py`
- `backend/content/test_free_demo_database.py`
- `backend/core/free_demo_ops_settings.py`
- `docs/AGENT_HANDOFF.md`
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
- `scripts/free_demo_database.py`
- `scripts/release_manifest.py`
- `scripts/verify_free_demo_database.py`


- `backend/requirements.in`
- `backend/requirements.txt`
- `backend/requirements-dev.txt`


25October patched-source final rerun: all33 Chromium journeys pass (15public/9integration/4sample/5student). Clean private export installs the regenerated hash locks with pypdf6.21.2, builds React and collects159 static files/459 post-processed. Npm runtime audit zero, full runtime/development pip-audit zero;19 canonical docs/271 release inputs validate. PostgreSQL17 guarded initializer and authenticated encrypted independent restore passed again with the patched environment. No original data, migrations, hosted credentials or deployment changes. The approved publication SHA and its matching CI outcome must be checked after the push; no earlier CI result substitutes for it.

---

# Current handoff — authenticated Render PostgreSQL audit

24 October2026. Local branch main and remote main both ff4acdc442cb971bd1e609433bd7de28488ddab1; preflight clean. This audit changes documentation only, uncommitted. Existing account kartikyasokhal28@gmail.com / My Workspace / Prepal project and Free web/database resources reverified. No live mutation, migration, seed, deletion, credential rotation, Git commit/push, redeploy or purchase. Verified private pre-edit documentation archive and audit results: ../.recovery/prepal-render-readonly-fecadz1d/.

Observed current service: branch main, auto-deploy Off, build bash deploy/render-build.sh, start bash deploy/render-free-demo-start.sh. Render PREPAL_ENVIRONMENT=free-demo, DJANGO_ENV=production, DEBUG=false, DATABASE_ENGINE=postgresql, exact external hostname dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com, POSTGRES_SSLMODE=verify-full, ALLOWED_HOSTS=rspc-ras.onrender.com, SITE_ORIGIN=https://rspc-ras.onrender.com. AI_ENABLED/AI_GUEST_ENABLED/STUDENT_FEATURES_ENABLED false. Existing SECRET_KEY and access-barrier variable names remain present; their private values were not revealed or changed. PREPAL_FREE_DEMO and PREPAL_FREE_DEMO_SYNTHETIC_DATA are absent on Render. Configuration changes since the previous handoff were owner-managed, not performed here. Four historical deploys still refer to038a4b2, all failed/canceled; ff4acdc is published, not deployed. No successful running commit is verified.

Actual authenticated connection used the existing ignored root.env connection credentials, overriding only the connection's host to the documented external endpoint (no file/env edits). libpq verify-full and pinned certifi CA succeeded; server17.11, TLS1.3/AES256-GCM. default_transaction_read_only was set at connection startup; transaction explicitly READ ONLY/REPEATABLE READ, verified read-only and rolled back. SELECT/catalog checks found only public schema, zero non-system tables/views/sequences/foreign tables/materialized views/routines/large objects, zero application rows, no django_migrations or auth_user tables. Therefore no application student/Admin accounts or content exist. Cluster has five login roles; those are PostgreSQL roles, not student accounts. Current configured role is not superuser/replication/BYPASSRLS, but has CREATEDB and CREATEROLE: do not use it as the deployed app runtime role. No SQL writes were performed.

The target is empty and suitable for disposable synthetic demonstration at audit time; setting both demo acknowledgements would be truthful if only the reviewed synthetic corpus/accounts are subsequently initialized. Flags are not deployment acceptance and were not set here. Recheck emptiness immediately before approved writes. Existing private root.env is mode0644 and still uses the internal host; its connection values/bytes were preserved. Restrict to0600 and use a dedicated protected operator config before future operations; do not load this root.env as a full free-demo app configuration. Original/archive/demo/media and the retired Django-key status remain unchanged. Current public network rules include0.0.0.0/0; narrow using verified Render egress/operator sources under separate approval. Free DB expires23November2026.

Verification for these documentation updates:10focused free-demo tests passed,19release documents/264inputs validate,secret scan0,17protected hashes unchanged,index empty. No full suite was rerun for documentation-only changes.

Exact next task: owner separately approves a guarded initialization implementation and existing-DB role/network/configuration changes. DEPLOYMENT specifies the30-migration empty-target plan and142-topic/15-lesson/75-question text-only corpus. Existing create_sample_content and rehearsal/provisioning/transfer commands deliberately refuse remote PostgreSQL: no ready remote seed command exists. Implement/review a dedicated guarded initializer reusing canonical corpus/publication/review/link services, test it against disposable PostgreSQL17, then separately authorize remote migrations/seeding/runtime credentials and manual deployment. Keep learner/AI/Google/uploads off, auto-deploy Off, secrets private, build/start non-migrating. Do not copy old demo DBs, PDFs, sessions, students or real data.

---

# Current handoff — approved main free-demo release

24 October2026. Current branch main, publication base038a4b2ff8a40b84b6d2c272b3c5835a1d793c5d; it contains the previous verified candidate1e685ee2a7b408fe6936dd0245fa776630d3286e and has the same application tree. Local main was fast-forwarded without resetting work. All264 approved inputs matched the previous manifest; a new private archive was hash-verified before edits. The release includes exactly the existing17modified/five new files plus publication updates within those documentation boundaries; no removed files, models/migrations/dependency-lock changes or unrelated code. Resolve this release commit with `git log -1 --format=%H -- docs/AGENT_HANDOFF.md`; verify origin/main equality and its own Actions result before acceptance. CI outcome is checked after publication and reported separately; pre-push local success is not remote CI evidence.

GitHub now shows Public. The owner explicitly approved publication to this public repository after disclosure of the visibility change and the known retired Django key in history. No active key is published, no old key is reused, and no history/visibility change is authorized. GitHub CLI is not authenticated; use the connected GitHub integration/browser for CI, SSH for the authorized normal push. Stop on new secrets, divergence or critical CI failure.

Verified designated Render account kartikyasokhal28@gmail.com / My Workspace / existing Prepal project and service srv-dbe6d5vb9u1s738ikh80, Free/Singapore. Auto-deploy changed from On Commit to Off and persisted across navigation before any push. Build remains bash deploy/render-build.sh, root empty, branch main, health/api/health/. Start remains bash deploy/render-start.sh: the requested free-demo switch is conditional and prerequisites currently fail (PREPAL_ENVIRONMENT=staging, internal POSTGRES_HOST, PREPAL_FREE_DEMO and PREPAL_FREE_DEMO_SYNTHETIC_DATA absent). No live environment, credential, DB or manual-deploy mutation occurred. Do not set a false synthetic-data acknowledgement to bypass the unaudited live database. Source/start prerequisites pass locally with synthetic test configuration; hosted readiness remains blocked.

Database blockers: use exact external hostname with verify-full/trusted CA; retain existing name/user/password and staging barrier. Previously verified external TLS1.3 is handshake-only, not authenticated SQL. Current roles/schema0001–0012/content/accounts remain unaudited because no usable private credentials were supplied; no SELECT or live SQL writes were executed. Review existing broad inbound access and expiring free PostgreSQL before acceptance. No migration/schema/seed command runs in build/start. No valuable uploads/student records are permitted; learner/AI/Google stay forced off.

This publication reran90frontend tests/lint/build,219Django discovered/214pass/five PG-only skips, system/migration checks,15public Chromium and four private free-demo smoke journeys. Initial sandboxed PDF test failed because the macOS memory-monitor command is restricted; unchanged full suite passed outside sandbox. The private fixture is SQLite with mocked services, not hosted PostgreSQL. Release/docs/staged checks and scans are required before commit. Production/staging/shared database policy and16protected file hashes remain unchanged. Private publication evidence: ../.recovery/prepal-free-publication-c0k7nsvh/; preserve earlier recovery.

Exact next task: after successful main CI, obtain an existing private credential-file path for authenticated read-only database audit, establish synthetic-only schema/content/roles status, then separately approve necessary live environment/network settings and any empty-target initialization. Only after prerequisites pass, save bash deploy/render-free-demo-start.sh with auto-deploy Off, and seek explicit manual deployment approval. Never migrate/reseed a valuable target, weaken TLS, buy services or trigger a deployment as part of this publication.

---

# Current handoff — local free Render demo preparation

24 October2026. Branch codex/prepal-1-0, HEAD1e685ee2a7b408fe6936dd0245fa776630d3286e; preflight working tree was clean. Current changes are local/uncommitted/unstaged. Owner now authorizes only a restricted free-demo candidate and inspection of existing free resources. No paid resource, service setting/secret mutation, commit/push, redeploy or live DB migration/cutover in this batch. Preserve previous protected data and production security.

Actual Render inspection under kartikyasokhal28@gmail.com / My Workspace tea-cv4hdkqj1k6c73bk2a50: Prepal project prj-dbdmln3ncjis73anntfg; Web Service RSPC-RAS- srv-dbe6d5vb9u1s738ikh80 in Staging evm-dbdmln3ncjis73anntg0, Free Python/Singapore; database prepal-staging-db dpg-dbe7a1oae00c73c5g090-a in the same project's db environment evm-dbe79j2vcj2c73bvgjo0, Free PostgreSQL17/Singapore/Available, expires23November2026. Do not move/duplicate resources. Current service tracks main at merge038a4b2ff8a40b84b6d2c272b3c5835a1d793c5d and auto-deploy On Commit. This was observed owner-managed state, not changed here; do not assume it follows the development branch. Last completed failure dep-dbe6hhhsrm7s73b2r6sg stopped at the staging environment guard before connecting to DB. The current non-secret settings now show production/staging, students=false, AI=false, verify-full/internal hostname; historical failed-deploy values are not proof of current values.

Prepared new backend/core/free_demo_settings.py, free_demo_support.py, free_demo_urls.py; deploy/render-free-demo-start.sh; backend/content/test_free_demo.py. Updated test_render.py to specify JSON for its unsupported-method assertion (free demo rejects all multipart requests), release_manifest.py to require new inputs, backend/.env.example and relevant existing docs. No models/migrations/dependency locks or production/staging/shared database security changes. Reuses render_support access barrier and reviewed SPA/static routes; text-only upload storage always refuses saves/opens/deletion, multipart is blocked before parsing, Admin content mutations403, staff login/logout remain available for synthetic staff only. Existing learner endpoint gate returns503 and Gemini/Google/email are disabled regardless of environment opt-ins. No database is seeded by build/start.

Required explicit profile selection: DJANGO_ENV=production; PREPAL_ENVIRONMENT=free-demo; PREPAL_FREE_DEMO=1; PREPAL_FREE_DEMO_SYNTHETIC_DATA=1; start bash deploy/render-free-demo-start.sh. Retain existing SECRET_KEY, STAGING_ACCESS_USERNAME/PASSWORD and database name/user/password. Use the exact external hostname and POSTGRES_SSLMODE=verify-full; default trusted CA is pinned certifi, or an existing explicit valid CA bundle. Reject internal hostname, lower SSL modes, missing acknowledgements/barrier or bad HTTPS origin. PRIVATE_MEDIA_ROOT env is preserved but unused; no upload directory is created. Missing schema/connectivity yields minimal health503 instead of leaking connection details. The profile is prepared, not selected on Render.

External host dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com passed actual PostgreSQL SSLRequest negotiation with CA and hostname verification: TLS1.3/TLS_AES_128_GCM_SHA256. No database authentication or SQL query occurred. Browser returns redacted credential placeholders; no usable DB credential was copied, exposed or changed. Owner was asked only for the path of an existing private environment file if authenticated read-only SQL is desired. Until supplied, do not claim roles/schema0012/content/accounts or SELECT1 were verified on the live database. Current external network rules show0.0.0.0/0; retain unchanged in this local-only task and review narrowing to service/operator addresses before accepting the demo. No TLS exception or require-mode fallback was added.

Exact next task: owner reviews local diff and remaining authenticated SQL/schema/synthetic-data audit. With separate explicit approval, select the new profile/external-host flags on the existing free service, decide manual auto-deploy policy, initialize only the reviewed synthetic target if needed, and redeploy a reviewed commit. There is no generic PostgreSQL production seed command in this batch: existing sample seeding deliberately refuses non-disposable/non-SQLite targets; do not bypass it or run migrations in builds. Free DB expires and has no production recovery guarantee; never store valuable user data/uploads here. No automatic commit/push/redeploy from this preparation. Paid plan and production backup/cutover remain separate future decisions.

Private verified recovery/evidence: /Users/kartikyasokhal/Downloads/MYPLACE/rpsc/.recovery/prepal-free-demo-zqihtnby. source-before.tar.gz/manifest verify259source files; protected.json covers16private original/demo/media/env files. New synthetic SQLite fixture is browser-demo; it is separate from active8002 and every original/demo archive. TESTING contains final actual results and limits. Previous publication source CI ran successfully39968769235 (including PostgreSQL17), but this new uncommitted profile has no new remote CI/deployment result.

Final local results:219Django discovered/214passed/five PG-only skips;90frontend tests/lint/build under vendor-verified Node24.22.0;15public Chromium plus4new-profile smoke journeys;system/deploy/migration checks pass;264release inputs and19release docs validate;Gitleaks0. Protected16hashes and all source production/staging/shared database policy/models/migrations/locks unchanged. Hosted health request timed out after12seconds (possibly cold-start delay); no successful hosted app or authenticated SQL/schema proof. No complete shell DB configuration was available. The only initial failures were the documented existing quiz signing-time fluctuation and the private Admin label selector; no test/security assertion was disabled.

---

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
