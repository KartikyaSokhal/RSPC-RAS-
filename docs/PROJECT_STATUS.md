## Current status — public-homepage release candidate, live approval still required

Reviewed from main baseline d2f014c186acba1360e9438a2382d13b85e74c6a. The local student-gated experience is included, with a separate exact-target hosted synthetic-login profile, read-only boot guard and transactional operator account extension. Git publication is authorized only after checks; authoritative publication SHA is `git log -1 --format=%H -- deploy/render-public-demo-start.sh`, with exact matching Actions results in the private publication receipt/GitHub. No live DB writes, Render changes or deployment in this batch. Render still runs d2f014c with Auto-Deploy Off and the old private barrier. Read-only hosted verification confirmed142 topics/15 lessons/15 quizzes/75 questions/300 choices/30 migrations/one staff/zero students/uploads. New private test password is prepared locally only; no account exists for it live. Exact configuration/SQL-operator approval gate is in DEPLOYMENT. Historical status entries below are not current activation authority.

---

## Current status — local student-gated preview, 25 October 2026

main remains d2f014c186acba1360e9438a2382d13b85e74c6a; this work is uncommitted and unstaged. Separate core.public_demo_settings prepares the requested public homepage/auth entry and student-only learning APIs/routes locally, using existing sessions and synthetic PostgreSQL accounts. Registration, recovery email, Google, Gemini, uploads and Admin edits stay closed. New local-only fixture contains142 topics/15 lessons/15 quizzes/75 MCQs/300 choices/two synthetic students/one view-only staff. No model/migration or hosted change. The earlier14 modified documentation files remain preserved. Verification and limitations are recorded in TESTING/AGENT_HANDOFF. Current Render Basic protection, Auto-Deploy Off, runtime credentials, TLS verify-full and expiring synthetic database were not altered. Older deployment-status blocks below are history.

---

# Current status — free synthetic demonstration LIVE

25 October 2026: the existing restricted demo is LIVE at https://rspc-ras.onrender.com. Render deployment dep-dbevgpfavr4c73c9m9i0 succeeded for main commit d2f014c186acba1360e9438a2382d13b85e74c6a at 18:11 IST. Matching GitHub Actions40171764725 is green. Account kartikyasokhal28@gmail.com / My Workspace / Prepal / Staging; existing Free web srv-dbe6d5vb9u1s738ikh80 and existing PostgreSQL dpg-dbe7a1oae00c73c5g090-a only. No new resource, purchase, upgrade, production release or valuable-data cutover.

Exactly30 migrations applied (content0001–0012 plus18 framework migrations),142 original syllabus topics/five subjects,15 sample note lessons,15 quizzes,75 questions,300 choices,19 tags,15 aliases,30 publications including ancestors,30 curated relationships and30 approved links. Exactly one synthetic view-only staff sample-editor, zero students/uploads/bookmarks/progress/saved attempts/AI requests. Engineering sample notices and quiz review reasons are not human academic approval.

PREPAL_ENVIRONMENT=free-demo, PREPAL_FREE_DEMO=1 and PREPAL_FREE_DEMO_SYNTHETIC_DATA=1; external PostgreSQL host dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com with POSTGRES_SSLMODE=verify-full and trusted CA. Build bash deploy/render-build.sh; start bash deploy/render-free-demo-start.sh; health /api/health/; Auto-Deploy Off. Production security profiles are unchanged. Student authentication/progress/planner/attempt saving, Google, Gemini/email, uploads and Admin content mutations remain disabled; the private staging barrier remains required.

Actual hosted Chrome checks passed: homepage142/five counts,142-link full expansion/five-root collapse, light/dark toggle, all15 sample lessons and their approved links/tags/related content, popup focus/new-tab attributes/Escape/focus restoration, three tag pages with exact counts, Monsoon search, all five subject practice pools and75/75 correct stateless scores, synthetic Admin login/session persistence/view-only detail/logout and five loaded Admin stylesheets. Config reports demo=true and student/AI/Google=false. Learner API error codes verified for guests and logged-in staff; Tutor request rejected as unavailable before provider work. HTTPS health200/status ok; unauthenticated homepage/config/Admin401 with Basic challenge, private/no-store/noindex; HSTS/nosniff/frame DENY verified. Keyboard skip-to-main, one main/one h1, no unnamed buttons and no horizontal overflow passed at1512px. This is a desktop browser smoke check, not a fresh mobile/axe/screen-reader/load audit.

Runtime/post-browser integrity and permission checks passed. Private evidence: ../.recovery/prepal-live-deploy-xjhhgl_i/. Documentation remains local/uncommitted; runtime source and HEAD unchanged, no purchase or valuable-data migration. Existing private data hashes are verified at final handoff.

Security incident and resolution: Render Copy value unexpectedly populated the staging password in browser accessibility output. It was not copied into source, documentation or evidence files. Owner confirmed replacing ONLY STAGING_ACCESS_PASSWORD with a new strong value using Save only; that replacement was not retrieved or displayed. Owner then completed native Chrome Basic sign-in and actual hosted tests succeeded. Do not reuse the exposed barrier value. Never use Render Copy/reveal controls for credentials in future automation; preserve passwords/signing keys, suppress secret-bearing AX field values and prefer owner native sign-in. No DB credential, recovery key/passphrase or Django signing key was exposed in this incident; the separately known historical Django key remains retired.

Owner explicitly waived permanent independent/off-device recovery-key custody ONLY for this disposable synthetic database; durable custody remains unconfirmed and production safeguards are not waived. A real read-only native pg_dump17.11 CMS AES256GCM snapshot now contains40tables/1237rows/zero uploads, encrypted to the dedicated owner certificate. Private snapshot/receipt are in ../.recovery/prepal-live-deploy-xjhhgl_i/hosted-encrypted-backup/. The dedicated key/restore tooling passed the earlier independent LOCAL PostgreSQL17 restore; this hosted snapshot was not restored live. No daily scheduler, off-host retention or production30-day guarantee is configured. Free cold starts/expiring DB remain unsuitable for valuable data.

Exact next task: owner reviews the restricted live demo. Before any new implementation, obtain separate scope approval. Known presentation limitation: existing homepage/banner/reader copy still mentions AI capability or “Verified study notes” although this demo forces AI off and notes explicitly require human review; do not interpret generic UI labels as academic approval. A separately approved demo-copy follow-up would touch src/components/layout/AppShell.jsx, src/pages/home.jsx, src/pages/topicPage.jsx and src/components/ai/TutorPanel.jsx. Do not start Phase5, enable learners/AI, change production secrets, introduce uploads, buy services or transfer valuable data automatically.

---

# Current status — recovery key prepared; live initialization still blocked

25October2026. main d2f014c186acba1360e9438a2382d13b85e74c6a unchanged; documentation-only work remains uncommitted. Exact hosted target passed authenticated read-only17.11/TLS/empty-schema/role checks. Zero live migrations or corpus rows/grants applied.

Dedicated10-year owner recovery recipient and passphrase-encrypted key prepared outside Git; encrypted-key transfer kit and private owner instructions ready. Real local17.11 restore verified40tables/1237rows/37sequences and exact approved synthetic corpus; wrong-passphrase/tamper checks passed. Off-device custody is NOT confirmed. Next: owner stores/retrieves/verifies kit off-device and separately stores its unlock secret, then confirms. No live initialization, Render changes/demo activation/deploy/purchases in this setup.

---

# Current status — approved recovery-test reliability follow-up

25October2026. main base6b29e39fc94d982309f307d64e7a6518d96b39e1. Five-file follow-up preserves four pending failure documents and changes only the recovery regression test. Controlled refresh confirms an assertion race; application navigation/authentication is unchanged. Twenty independent runs passed, as did90frontend/lint/build,224 PostgreSQL17 backend,219 SQLite/five PG-only skips, guarded initializer/encrypted restore, migration/system and zero-finding runtime/development security checks. See TESTING for final browser/release evidence. Normal publication is approved after checks; verify the exact new SHA/CI rather than reuse the parent failure or earlier success. Next gate remains live initialization plus durable key custody approval, then separately approved Render configuration/manual deployment. No live mutation, feature activation or purchase.


Final local result: all33 Chromium journeys pass (15public,9integration,4sample,5student), plus20independent recovery-test runs and90frontend tests/lint/build.19 canonical documentation files/271 release inputs validate; exact five-file scope and preservation of all four pre-existing documentation updates verified. No source/history scanner findings; independent staged private-value checks are mandatory before commit. All17 protected hashes and other tracked runtime/config/model/migration/dependency files are unchanged. Publish normally only after staged checks and verify the exact new CI run; live initialization/deployment remain separate approval gates.

---

# Current status — published; CI acceptance blocked

25October2026 post-push result: commit6b29e39fc94d982309f307d64e7a6518d96b39e1 is normally pushed to main; remote SHA matches. [CI40169515420](https://github.com/KartikyaSokhal/RSPC-RAS-/actions/runs/40169515420), job121097333587, FAILED at npm run check:89frontend passed/one failed. Backend, PostgreSQL17 initializer and browser CI steps were skipped. Do not call this release CI-accepted or use prior CI as acceptance. No CI retry or follow-up code change was made after failure; owner stop gate applies.

Failure: src/test/student-platform.test.jsx:91, recovery-fragment/session-refresh test expected "Password changed. Sign in with your new password." but received intermediate "Password changed." ResetPasswordPage sets its status before awaiting refreshStatus and navigating; findByRole('status') can resolve against that intermediate element. Timing-race diagnosis is inferred from the exact log/code, not a proven product failure. These frontend files are byte-identical to the parent commit and were outside this28-file release; local90tests and33Chromium passed. Do not weaken assertions, blindly retry CI or change product authentication behavior.

Exact next task needs approval: narrowly update src/test/student-platform.test.jsx to await completed login navigation/final status before asserting the unchanged full success message and session-refresh call, run focused/full frontend checks and regressions, review the extra test-file diff, then commit/normal push and verify its own CI including PostgreSQL17. Until then stop publication/deployment/live initialization. The following pre-push local verification remains valid for its stated environment only.

---

# Current status — security patch verified for initializer publication

25 October2026. main publication base ff4acdc442cb971bd1e609433bd7de28488ddab1; owner approves normal commit/push after exact28-file/security verification (previous25 plus3 dependency files). Resolve release SHA from git log -1 --format=%H -- backend/requirements.in and verify origin/main/Actions. No predeclared remote CI success.

Approved pypdf6.21.2 patch and two regenerated hash locks change no other package pins. Runtime/development audits zero; pip check clean.31focused PDF/content/Admin regressions,224 PostgreSQL17 backend,219 SQLite passes/five PG skips,90frontend/lint/build,11 initializer/recovery assertions, transfer/concurrency checks pass. Final Chromium/clean-export/security evidence is recorded in TESTING. Original data/migrations/production policy preserved. No hosted changes or deployment; Auto-Deploy Off. Next gate: matching release CI, durable recovery recipient/key custody, explicit guarded live initialization approval, later separate Render configuration/manual-deploy approval.


25October patched-source final rerun: all33 Chromium journeys pass (15public/9integration/4sample/5student). Clean private export installs the regenerated hash locks with pypdf6.21.2, builds React and collects159 static files/459 post-processed. Npm runtime audit zero, full runtime/development pip-audit zero;19 canonical docs/271 release inputs validate. PostgreSQL17 guarded initializer and authenticated encrypted independent restore passed again with the patched environment. No original data, migrations, hosted credentials or deployment changes. The approved publication SHA and its matching CI outcome must be checked after the push; no earlier CI result substitutes for it.

---

# Current status — authenticated free-demo database audit

24 October2026. main/local/remote ff4acdc442cb971bd1e609433bd7de28488ddab1; no new commit/push. Current Render environment/host/start now match free-demo/external verify-full/render-free-demo-start.sh; build unchanged, auto-deploy Off. Both demo acknowledgements are absent. Four historical failed/canceled deploys still reference038a4b2; current release is not deployed.

Authenticated read-only PostgreSQL17.11/TLS1.3 verify-full checks passed: zero application tables/rows/users/content, no migrations applied. Empty target is suitable for synthetic-only demo acknowledgements, but schema/content must be initialized under separate approval. Configured role has CREATEDB/CREATEROLE; limited runtime role and network restrictions remain blockers. Existing seed tools are local/SQLite-only; guarded remote initialization is not implemented. No live data/settings or private files were changed. See DEPLOYMENT, SECURITY, TESTING and newest handoff. Current edits are documentation only.

---

# Current status — approved free-demo publication on main

24 October2026. main was fast-forwarded to remote merge038a4b2 (identical tree to verified1e685ee); all264 approved release inputs matched before publication-only documentation edits. Owner explicitly approved the now-Public GitHub destination, including disclosure of the known retired key's historical presence. Release SHA/remote equality and CI must be verified after the approved normal push; this document does not predeclare CI success.

Render auto-deploy is now Off (saved and verified), build unchanged. Start-command switch is blocked by current staging/internal-host configuration and missing free-demo acknowledgements; no redeploy, environment/secret edits or live DB SQL. Schema/data/roles remain unaudited. Next: authenticated read-only synthetic-target audit, separately approved configuration/initialization, then manual deployment approval. Local tests/security and limits are in TESTING and the latest handoff.

---

# Current status — free-demo candidate, 24 October 2026

Local clean baseline codex/prepal-1-0 at1e685ee2a7b408fe6936dd0245fa776630d3286e. New restricted free-demo settings/storage/HTTP guard/start script/tests are prepared locally; current work is uncommitted/unstaged and no redeploy is authorized. Production, staging and shared TLS settings are unchanged. No models/migrations or live DB changes.

Existing owner-managed Render service is Free/Python/Singapore at srv-dbe6d5vb9u1s738ikh80, tracks main/038a4b2 with auto-deploy On Commit. Existing Free PostgreSQL17 dpg-dbe7a1oae00c73c5g090-a reports Available and expiry23November2026. Account is the designated email; resources remain in the original Prepal project. Earlier documentation describing an empty project is historical.

External PostgreSQL TLS1.3/CA/hostname verification passed without authentication or SQL. Current internal-host/verify-full combination is unsupported by Render; the new profile requires the verified external endpoint and trusted CA, with no weaker TLS exception. Authenticated SQL/schema/content are pending an existing private credential file; do not claim live DB acceptance. Current service has no verified successful deployment; last failure preceded DB access. Free candidate disables learner/AI/Google, uploads and Admin editorial mutations and has no valuable ephemeral storage. Actual local test results are in TESTING. Next: review local changes and obtain separate commit/push/live configuration/bootstrap/redeploy approval after authenticated synthetic-data checks.

Final local verification:214backend passes/five PGskips;90frontend;15public+4free-demo Chromium;lint/build/system/deploy/migration checks;264release inputs/19docs;secret scan0;16protected hashes unchanged. Hosted health probe timed out after12seconds and authenticated SQL remains unverified; no deployment acceptance claim.

---

# Current status — approved development-branch publication

23 October 2026: the owner approved the reviewed staging candidate for a verified local commit and normal push to codex/prepal-1-0. Preflight local/remote base8ef43c7e945d8d81d232b44583990b69f82519ff, zero divergence,259reviewed files unchanged. This section travels with the release commit; obtain the release SHA from Git and confirm the matching GitHub Actions run. Publication/CI outcomes are verified after push, not inferred from historical runs. No hosted service, paid provisioning, production deployment, main merge or data cutover is authorized. Next gate: separate Render repository-access and paid staging approval after successful CI. Previous status sections are historical.

---

# Current status — restricted Render staging candidate

**Actual non-billable dashboard action:** created [Prepal project](https://dashboard.render.com/project/prj-dbdmln3ncjis73anntfg) with the empty Staging environment evm-dbdmln3ncjis73anntg0 in the verified workspace. Verified zero services and zero environment groups. This is an organizational container, not a running deployment; no charges, credentials or data were added. Reuse this project on the next turn.

23October2026: local and remote branch codex/prepal-1-0 remain at8ef43c7e945d8d81d232b44583990b69f82519ff; all work remains uncommitted and unstaged. Designated Render/Vercel accounts verified. No existing Prepal deployment found. Commercial/client use selects single-origin Render web+PostgreSQL17+private disk, estimated$13.55/month base excluding tax/overages/backup storage. Render GitHub integration does not yet include this private repository. Only the free project container and empty Staging environment were created; no compute/database service was provisioned or deployed.

Prepared guarded Render settings/routes/access barrier and non-migrating build/start/static configuration. Owner-approved sanitized root.env.example restored. Fixed actual CI conversation-scroll accessibility defect and4dependency advisories with DRF3.18.2/certifi2026.10.19; WhiteNoise6.12.0 added. Current local results:204backend passes/5PGskips,90frontend,15public+5student Chromium, real loopback Gunicorn smoke, dependency/secret/docs/release checks. See TESTING for limits and exact evidence. No source models/migrations/data changes in this batch.

Next: owner approval of release commit/push, narrow Render repository access and recurring resource costs. Then new empty staging schema0012 with verified external PostgreSQL TLS/restricted roles, durable media and restricted HTTP access; synthetic hosted acceptance via explicit Render-only student test gate. Production remains closed. Daily encrypted30-day retention target is approved but hosted storage/schedule/alerts/restore remain outstanding. Gemini/Google/SMTP credentials/requests and valuable data cutover stay gated.

---

# Current status — PostgreSQL preparation, no cutover

23 October2026. Branch codex/prepal-1-0, committed HEAD8ef43c7e945d8d81d232b44583990b69f82519ff unchanged; all prior uncommitted work remains. Safe local PostgreSQL configuration/provisioning/security and encrypted backup/restore rehearsal are implemented and verified. Active8002 remains core.student_demo_settings on isolated SQLite ../.recovery/prepal-student-platform-yeqsw05q/student-review/demo.sqlite3, schema0012. At preflight/final check: one synthetic staff editor, zero student identities/sessions/bookmarks/progress/attempts/plans/tasks;142topics/200questions/800choices. No current real student data was transferred or overwritten.

Verified source backup/restored copy imported39tables/2,433rows with exactIDs/FKs and37sequence counters into NEW PostgreSQL16.2. Synthetic accounts/learning data survived two backend starts and independent encrypted native restore:39tables/2,467rows/37sequences and one test media file. Separate migration/runtime/backup roles and bounded timeouts; backup role does not receive application signing key. Guarded staging/production stay learner/AI/Google closed. Models/migrations0001–0012 unchanged by this task.

Current checks:204 PostgreSQL passed;199 SQLite passed/five PG-only skips;90 frontend tests/lint/build;15fixture+five student Chromium passed. System/migration consistency and26protected hashes pass. [TESTING](TESTING.md) holds commands/evidence and intermediate diagnoses. Private task evidence/recovery is ../.recovery/prepal-postgres-security-d5oj1nit/; temporary PG cluster is stopped after verification, not installed as a persistent service.

Pending owner gates: approve deletion and retention policy before irreversible behavior; approve source/content and persistent PostgreSQL17 target/roles/CA, durable off-host storage/schedule/alert/restore/RPO/RTO before real cutover. No production backup or scheduler is activated. Resolve existing missing root .env.example separately; release completeness remains blocked. Academic review, real SMTP/Google/email-verification and production security acceptance remain. No paid request, commit/push/deploy or automatic next phase.

---

# Local authentication navigation — 23 October 2026

Active frontend: http://127.0.0.1:5173; explicitly selected student API: http://127.0.0.1:8002. The old content-only backend8000 still returns learner=false. Vite now selects the student backend via ignored development-only configuration; the public config endpoint confirms learner=true and Google=false. Normal development/production settings default closed. Existing student routes/owned functionality are reused; no original data/model/migration changes or release operation.

Current navigation-task results and exact startup/evidence are in TESTING and AGENT_HANDOFF. Root .env.example was already deleted at preflight and remains untouched: full release manifest/check_docs --release is blocked, separately from working app navigation. Historical full-platform results below remain historical.

# Project status — 23 October 2026

Current branch: codex/prepal-1-0. Committed HEAD: 8ef43c7e945d8d81d232b44583990b69f82519ff. Student-platform work is local/uncommitted; no current commit, push, deployment, real cutover or paid request.

Modules 1–7 are implemented locally: session/Google/reset adapter, owned dashboard/bookmarks/completion/visits, deterministic planner, isolated new corpus, immutable saved canonical practice and strict current-note Tutor. Production student gate defaults off; existing content-only demos stay off. Old ownerless rows remain inaccessible. Modules 8–11 cover disposable migrations/restore, targeted responsive/accessibility regression and this canonical handoff; actual final results are in TESTING.

Content: 25 additional real-syllabus lessons (five per root), 125 MCQs/500 choices. They are isolated unpublished/in_review drafts, with draft aliases/relations, no new quiz approval and a private source/review inventory. Existing 15-lesson sample is preserved. Human academic/rights review is pending; do not promote synthetic sample approvals.

Source migrations end at 0012. Original 0001–0008 are unchanged; original SQLite remains 0004 and all existing demos/media are protected. New migrations ran only on disposable/new review targets. PostgreSQL is still normal runtime; no real cutover happened.

Google consent/credentials, SMTP delivery and live Gemini are not externally verified. Current Gemini tests use mocks; no request budget is approved. Password email verification policy, production roles/TLS/backup/host/media/proxy timeouts, load/manual accessibility and final deployment acceptance remain open.

The previous repository-presentation cleanup remains a proposal: no destructive cleanup/moves were executed. Private verified pre-task archive/evidence is ../.recovery/prepal-student-platform-yeqsw05q/. Preserve it and all older recovery records. Exact continuation: owner review of current diff; human content review and configured-service acceptance on an approved test environment before any separate release/cutover/deploy authorization. See [handoff](AGENT_HANDOFF.md), [roadmap](IMPLEMENTATION_PLAN.md), [testing](TESTING.md).
