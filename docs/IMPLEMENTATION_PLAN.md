# Implementation roadmap and checklist

Current authority is the approved documentation cleanup, not a feature phase. Base HEAD: `49407b2dcbf94a7d255bbc702afe039071ff65e7`, branch `codex/prepal-1-0`. No commit, push, merge, history rewrite, database migration, production change or deployment. Stop after verification and owner review.

## Current cleanup acceptance

- [x] Verify the exact approved 12 removals/16 edits against a clean base.
- [x] Privately archive all 28 affected originals; verify every archive member and an independent restore before removal.
- [x] Preserve active task requirements here and current UI/accessibility constraints in ARCHITECTURE.
- [x] Remove only the approved retired documents and update all remaining references; retain 19 canonical Markdown documents.
- [x] Harden only the approved ignore patterns; keep source/templates/docs/migrations trackable.
- [x] Complete frontend/backend/lint/build, docs/Git/secret checks and verified 211-file release export; record actual results in TESTING/status/handoff.
- [ ] Owner reviews resulting uncommitted diff and security findings, then separately decides whether to authorize a cleanup commit.

## Completed foundation (historical, retained requirements)

| Work | Existing implementation / boundary |
|---|---|
| Safe foundation | SafeHtml/Markdown, stable reviewed quiz retrieval/grading, learner-state containment; no ownerless records exposed |
| Phase 1 | PostgreSQL configuration and disposable transfer/restore rehearsal; migrations 0001–0006 preserved; no real cutover |
| Phase 2 | Django Admin/editor/review/publication, normalized tags/aliases, stable reviewed TopicRelation and canonical Question associations; migration 0007 |
| Phase 3 | Evidence-bound phrase proposals/derived scans, publication-aware popups/tags/related topics and deduplicated topic/subject practice; migration 0008 |
| Phase 4B | Shared hierarchy, original-order numbering/expansion, subject navigation, honest counts, Search/theme shell and one Tutor launcher |
| Sample content | Separate five-subject/142-topic demo; 15 referenced lessons, 75 MCQs, 19 tags, 15 aliases, 30 approved links/relations; strict no-overwrite seed |
| Controlled cleanup | Private recovery, retired backend/environment archival, unused starter/generated artifact removal, seven unused imports, honest count regressions, sanitized capture and release tooling |
| Master Phase A | Committed release 49407b2; local exposed-key retirement and nine session/signature checks; no push |

Review existing sample material academically; engineering approval never substitutes for human content/rights review. Keep original/demo data, private backups/evidence, migrations and dormant learner code. Pending learner releases require separate scope.

## Remaining master sequence and gates

| Phase | Exact next scope | Approval/status |
|---|---|---|
| A cleanup follow-up | Review this documentation/ignore-only diff; proposed message: Consolidate Prepal documentation and harden release exclusions | Uncommitted; no commit authorized |
| B | Reverify approved commit/remote, obtain separate push approval, push without history rewrite, compare remote SHA and inspect CI | Blocked pending owner release/security review; SSH read access previously worked, gh CLI unauthenticated |
| C | Published-snapshot topic-note PDF export; strict server-side current-topic Tutor; grounded citations, refusals, quotas and mock/security regressions | Not started; follows preceding gates; no paid provider calls without explicit budget/credentials |
| D | Owner-approved production dataset, PostgreSQL target/roles/TLS, encrypted durable backup/retention, fresh backup/restore/rehearsal/rollback | No real transfer/connection switch until explicit approval; never include demo/learner records by assumption |
| E | Approved provider/domain, HTTPS/proxy/static/private media/Admin/monitoring, persistent recovery and PDF timeout alignment | No billable provisioning or credentials assumed |
| F | Approved staging; full functional/security/accessibility/load/restore/rollback checks; separate final production approval | No staging or production deployment |

Before any Git publication, review that audited remote main still contains a retired key and old implementation; current development refs lack later local work. Ordinary future release updates cannot erase old history. Purging history, external credential rotation, live AI spend and production cutover remain separate explicit decisions. See [security](SECURITY.md), [deployment](DEPLOYMENT.md) and [handoff](AGENT_HANDOFF.md).
