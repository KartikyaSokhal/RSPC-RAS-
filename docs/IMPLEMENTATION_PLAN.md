## Current approved batch — main free-demo publication

Owner explicitly approved the verified free-demo candidate to main and, after current inspection, the now-Public GitHub repository. Preserve previous candidate/history and use normal fast-forward push only. Keep Render auto-deploy Off (now saved); preserve build command and secrets. Current free-demo start prerequisites fail, so switch remains deferred. No redeploy/live DB migration/schema/write or paid service is authorized. Next: authenticated read-only target audit, review synthetic-only initialization/configuration separately, then approve manual deployment after passing prerequisite checks. Read latest handoff and DEPLOYMENT before any live action.

---

## Current local batch — free Render demonstration

Completed local implementation: separate explicit free-demo profile/start; verified external-host TLS/CA requirement; existing password barrier and SPA/static reuse; learner/AI/Google disabled; rejected uploads/direct storage/Admin mutations; safe DB readiness and focused regression coverage. Actual hosted resources/settings were inspected without edits. No live SQL/authenticated schema audit was possible with redacted credentials; owner can identify an existing private local environment file, without pasting secrets.

Next sequence after local review: authenticate/read-only audit actual PostgreSQL schema and synthetic-only contents; separately approve any Git publication, live profile/host changes and empty-target synthetic initialization; then approved redeploy and hosted acceptance. Current service tracks main with auto-deploy On Commit, so publication/config changes could trigger deployment and require explicit coordination. Do not weaken TLS, bypass seed-tool safety guards, purchase storage or transfer real data. Keep production security and backup/cutover gates unchanged.

---

## Current approved batch — staging release publication

Commit the exact reviewed staging candidate after staged-diff/secret/exclusion verification, normally push codex/prepal-1-0, compare remote SHA and inspect that commit's CI. Stop on new secrets, divergence or critical CI failure. Documentation and required source dependencies belong to the candidate; no new feature implementation. After passing CI, the exact next task is separately approved Render repository-access and paid staging setup. No main merge, real cutover, paid AI or production deploy. Earlier Git approval gates below are superseded only for this candidate.

---

# Implementation roadmap and checklist

## Current authorized batch — student platform

23 October 2026, local work over 8ef43c7 on codex/prepal-1-0. Preserve Phase 1–4 and all existing data. No commit/push/deploy/real cutover/paid provider request.

| Module | Local implementation | Acceptance evidence |
|---|---|---|
| 0 | Verified source/data snapshot and baseline | Private recovery archive/manifests; baseline 80 frontend, 121 backend/four skips |
| 1 | Sessions, password registration/login/logout/reset, Google state/nonce/PKCE/signed claims, identity and rate limits | Mock provider, CSRF, duplicate/collision/replay and session tests |
| 2 | Real owned dashboard, counting, weighted scores, continue/recent/next/subject summaries | Empty-account, published eligibility and ownership regressions |
| 3 | Owned bookmarks/completion and explicit visits | Idempotence, rejected writes, no adoption and logout isolation |
| 4 | Deterministic owned planner, estimates and rescheduling | Calendar/capacity/default/feasibility/history/isolation tests |
| 5 | 25 new sourced lessons and 125 MCQs in isolated review | Validation/idempotence/mapping/private-draft barrier; human academic approval pending |
| 6 | Saved immutable practice snapshots with UUID idempotence | Canonical grading, edits/deletions/history, ownership and guest regressions |
| 7 | Strict current-note Tutor and selection/prompt safety | Cross-topic refusal, citations, mock timeouts/quotas; no live provider request |
| 8 | Additive reversible migrations 0009–0012 | Disposable PostgreSQL forward/reverse, source-copy and restore checks |
| 9–10 | Targeted responsive UI and regression/accessibility tests | Actual environment-labelled results in TESTING |
| 11 | Existing canonical documentation and handoff updated | Release documentation/manifest validation |

Historical P000–P003 and Phases 1–4 delivered safe HTML/Markdown, learner containment, reviewed deterministic practice, PostgreSQL configuration, Admin/content metadata, approved discovery and targeted UI. They remain regression requirements. Earlier master Phase A was 49407b2; documentation cleanup baseline became 8ef43c7. The development branch was published under separate prior authority; that does not authorize publishing current uncommitted work.

## Next approvals and sequence

1. Owner reviews this local implementation and exact diff/test evidence. Any commit and push require separate approval; do not rewrite history.
2. Human editor reviews the new corpus, MCQs, references/rights, aliases and relationship proposals in the isolated Admin. Publish/review explicitly; regenerate and inspect approved connections. Do not copy synthetic engineering approvals into production.
3. Configure Google consent/client/callback and SMTP on an approved test origin. Validate real consent/collision/logout/reset-delivery/session behavior. Decide password-account email-verification policy.
4. Approve a Gemini model, compatibility, current pricing and bounded request budget before live tests. Evaluate grounding/refusal/citations with current lesson only.
5. Select real source and PostgreSQL target/roles/TLS; approve fresh coherent DB/media backup, restore and rollback rehearsal. Apply migrations/cutover only with explicit authorization. Existing data remains immutable meanwhile.
6. Approve hosting/domain/billing, private media/static/proxy timeouts, monitoring and staging. Verify staged security/accessibility/operations before separate final deployment acceptance.

Topic-note PDF export is still deferred. The repository-presentation cleanup is a separate unapproved proposal; do not remove current docs or source. Significant history remains in [DECISIONS](DECISIONS.md) and [CHANGELOG](CHANGELOG.md); [handoff](AGENT_HANDOFF.md) is the continuation entry point.

## Local navigation restoration — 23 October 2026

Completed targeted local configuration/navigation: selected ready student environment, disabled implicit normal-development opt-in, reused existing account routes, preserved production closure and added guarded startup/proxy and navigation/session/mobile regression coverage. No new product module, database migration or release operation. Remaining next steps are still owner review and separately approved content/external-service/production acceptance.

## Current PostgreSQL/security task

- Completed locally: actual8002 database/count inventory; verified source/media backup and new-directory restore; separate-role PostgreSQL provisioning/config/timeouts; copied-source schema+transfer; student persistence/restart/isolation; encrypted native backup/independent restore and security regressions; readiness-only deletion gate.
- Pending approval: proposed deletion/backup-retention policy before any irreversible implementation. No deletion/pruning is enabled.
- Pending cutover packet: owner-approved real source/content and target/roles/CA; fresh frozen backup; PostgreSQL17+TLS and durable off-host restore/failure-alert acceptance; explicit configuration switch approval. Production students/Google/AI stay off. No automatic next phase, Git release or deployment.
- Pre-existing release blocker: missing root .env.example; resolve separately without discarding uncommitted work.

## Current next batch — review Render candidate

Local staging code and access inspection are complete pending final verification in TESTING. Next: owner review and explicit commit/push, narrow Render GitHub repository grant and recurring-resource approval; new empty PostgreSQL17/roles/TLS/private disk; approved migrations/deploy; hosted smoke/security/accessibility/backup verification. Never use free expiring PostgreSQL for durable data. Existing source templates and guarded local backup tools do not establish hosted backup acceptance. No automatic student or production activation.
