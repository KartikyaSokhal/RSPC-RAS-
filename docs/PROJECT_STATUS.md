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
