## Current hosted-demo scope

Publish the reviewed candidate to main after release/secret checks and require matching fully green GitHub CI. Prepare only an existing-resource public-homepage profile with one private synthetic test identity; no real enrollment, new paid resource or production launch. Live account/marker/grant writes, Render configuration changes and manual deployment remain separate approval gates. Existing private staging and local-only review profiles remain supported. Nonexpiring data storage, independent recovery/retention and public-auth/security/privacy operations are still prerequisites for real students.

---

## Current local-only expansion

The student-gated visitor experience is authorized for isolated synthetic review, not live registration. Homepage/auth entry pages are public; learning library and owned records require a student session. Sign Up remains accessible with registration closed. Existing content-first and private staging/free-demo profiles remain supported and unchanged. Real students require persistent nonexpiring PostgreSQL, independent backup/recovery custody and rehearsal, operational/security acceptance and separate deployment approval. No external service or hosted profile activation belongs to this batch.

---

## Current scope — deployed disposable synthetic demo

25 October 2026: the existing restricted demo is LIVE at https://rspc-ras.onrender.com. Render deployment dep-dbevgpfavr4c73c9m9i0 succeeded for main commit d2f014c186acba1360e9438a2382d13b85e74c6a at 18:11 IST. Matching GitHub Actions40171764725 is green. Account kartikyasokhal28@gmail.com / My Workspace / Prepal / Staging; existing Free web srv-dbe6d5vb9u1s738ikh80 and existing PostgreSQL dpg-dbe7a1oae00c73c5g090-a only. No new resource, purchase, upgrade, production release or valuable-data cutover.

PREPAL_ENVIRONMENT=free-demo, PREPAL_FREE_DEMO=1 and PREPAL_FREE_DEMO_SYNTHETIC_DATA=1; external PostgreSQL host dpg-dbe7a1oae00c73c5g090-a.singapore-postgres.render.com with POSTGRES_SSLMODE=verify-full and trusted CA. Build bash deploy/render-build.sh; start bash deploy/render-free-demo-start.sh; health /api/health/; Auto-Deploy Off. Production security profiles are unchanged. Student authentication/progress/planner/attempt saving, Google, Gemini/email, uploads and Admin content mutations remain disabled; the private staging barrier remains required.

Exactly30 migrations applied (content0001–0012 plus18 framework migrations),142 original syllabus topics/five subjects,15 sample note lessons,15 quizzes,75 questions,300 choices,19 tags,15 aliases,30 publications including ancestors,30 curated relationships and30 approved links. Exactly one synthetic view-only staff sample-editor, zero students/uploads/bookmarks/progress/saved attempts/AI requests. Engineering sample notices and quiz review reasons are not human academic approval.

Owner approved initialization of the exact empty demo DB and manual deployment after restricted runtime selection. Both completed and hosted acceptance passed; no valuable-data cutover, paid service or automatic Phase5. Owner explicitly waived permanent independent/off-device recovery-key custody ONLY for this disposable synthetic database; durable custody remains unconfirmed and production safeguards are not waived. A real read-only native pg_dump17.11 CMS AES256GCM snapshot now contains40tables/1237rows/zero uploads, encrypted to the dedicated owner certificate. Private snapshot/receipt are in ../.recovery/prepal-live-deploy-xjhhgl_i/hosted-encrypted-backup/. The dedicated key/restore tooling passed the earlier independent LOCAL PostgreSQL17 restore; this hosted snapshot was not restored live. No daily scheduler, off-host retention or production30-day guarantee is configured. Free cold starts/expiring DB remain unsuitable for valuable data.

Exact next task: owner reviews the restricted live demo. Before any new implementation, obtain separate scope approval. Known presentation limitation: existing homepage/banner/reader copy still mentions AI capability or “Verified study notes” although this demo forces AI off and notes explicitly require human review; do not interpret generic UI labels as academic approval. A separately approved demo-copy follow-up would touch src/components/layout/AppShell.jsx, src/pages/home.jsx, src/pages/topicPage.jsx and src/components/ai/TutorPanel.jsx. Do not start Phase5, enable learners/AI, change production secrets, introduce uploads, buy services or transfer valuable data automatically.

Older authorization sections below are historical; they never activate production/student/AI functionality.

---

## Approved staging branch publication

The owner authorized committing and normally pushing the reviewed staging candidate after final staged security/diff checks. This includes its required student-platform source/migrations and tested staging configuration; it does not authorize unrelated implementation. Render GitHub access instructions only, no permission grant. Paid infrastructure, real data cutover, production launch, main merge and billable Gemini remain excluded. Stop if release security/divergence/critical CI checks fail.

---

# Student platform scope

The 23 October 2026 full student-platform request supersedes the older content-only authorization. Retain React/Vite, Django/DRF, Django Admin, PostgreSQL and the existing published-content/discovery architecture. No new admin SPA, search system or unrelated redesign.

Locally implemented: secure sessions and Google OAuth adapter, reset flow, owned dashboard/bookmarks/completion/visits, deterministic planner, reviewed canonical practice with saved immutable student attempts, and current-published-lesson-only Tutor. Guest practice stays stateless. Production student access is opt-in; old demos retain their closed gate. No ownerless data adoption.

New content is authored only in an isolated review environment: 25 new lessons/125 MCQs plus source and review inventory. It has no fabricated human approval or automatic publication. The preserved 15-lesson synthetic sample remains separate from real production editorial approval.

Counting is consistent: current published notes or approved attached PDFs form learning units; empty headings do not. Planner task completion is tracked separately from marking a whole lesson completed. Missing duration uses an explicitly approximate editable default.

Current Tutor excludes other lessons, related documents, PDF evidence, website-wide retrieval and external tools. Links/related content remain reader navigation only. Live AI defaults off; a paid request needs explicit provider/model/budget approval. OAuth and SMTP are implemented with mocks but await owner configuration and external acceptance.

Deferred: phone OTP, topic-note PDF export, production email-verification policy, human review/publication, real PostgreSQL cutover and deployment. Preserve original SQLite, all existing demos/media/archives and migrations 0001–0008. New migrations 0009–0012 are permitted only on disposable/new review targets in this task. No commit/push/deploy/production secret change/paid requests are authorized. The prior repository-presentation cleanup proposal remains unapproved; no deletions or moves are performed.

[Features](FEATURES.md), [roadmap](IMPLEMENTATION_PLAN.md), [handoff](AGENT_HANDOFF.md).

## PostgreSQL preparation boundary

Local PostgreSQL persistence/recovery rehearsal is implemented without switching the active student-review SQLite. Production profiles force learner/AI/Google off. Account deletion is non-destructive readiness only, pending owner-approved policy; production off-host backup/scheduling/monitoring and real cutover remain separate gates. This task does not approve public student release, paid providers, Git publication or deployment.

## Current hosting preparation authority

Owner authorized account inspection, local deployment configuration and a reviewable release candidate. Commercial/client use excludes Vercel Hobby. Selected Render same-origin staging needs separate paid-resource and Git release approval. Sanitized frontend.env.example restoration is approved. No production launch, real cutover or student activation is implied. Daily encrypted30-day production backup retention is the approved target; provider/scheduler/restore acceptance remains outstanding.

Render-only synthetic student acceptance has a separate explicit two-flag/database-name/private-access guard; normal staging and production remain closed. No hosted flags were enabled.
