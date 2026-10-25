## Guarded free-demo security and initialization preparation

Only existing Render Free resources/account/main are in scope. Owner approved credential0600, separate restricted DB roles and scoped DB networking; these security preparations are complete. No live app schema/migrations/corpus/Render env/redeploy or paid service is authorized. A guarded operator-only initializer and encrypted manual recovery workflow are prepared/tested locally; actual local17.11/native recovery checks pass; live initialization approval, durable recovery key custody and new CI remain. Approved pypdf6.21.2 input/hash-lock patch passes audits and PDF regressions; normal publication is authorized after checks, no unrelated upgrades. One view-only synthetic staff, no learner functionality or uploads, and engineering-only sample review labels are mandatory. See current DEPLOYMENT/handoff; older local-only authority below is historical.

---

## Current free-demo scope

Owner selected existing Free Render web/PostgreSQL17 resources only. Prepare changes locally; no purchases/upgrades, Git release, live configuration/redeploy, DB initialization/write/cutover. New profile must preserve production-strength settings, existing barrier/secrets, strict TLS and synthetic-only content while disabling student/AI features and uploads. No durable private media or production user data on free resources. External verified TLS is available; no require-mode exception is approved or implemented. Previous paid architecture remains a future production option, not current authority.

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
