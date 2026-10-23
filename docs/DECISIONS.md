# Decisions and significant history

Current authority is safe local implementation of the full student platform, not deployment/publication/cutover or paid provider requests. Historical approvals below never bypass the latest owner brief.

## 23 October 2026 — owned student platform

Reuse Django User/sessions and existing learner records with strict ownership; never adopt NULL owners. Add StudentIdentity rather than replace User. Google linking is deliberately explicit/manual on collisions; provider tokens are not retained. Production student gate defaults off, older demos remain content-only. SMTP and Google are mocked until configured and externally accepted; password-account email verification policy remains an owner decision.

Use one content-bearing published-unit counting rule. Planner schedules deterministically, marks estimates approximate and preserves completed work separately from whole-lesson completion. Save immutable answer/classification snapshots under existing QuizAttempt with per-user UUID idempotence; guest grading stays stateless and questions canonical.

Tutor scope is narrowed to current published notes only, including no PDF or related retrieval. No paid test without model/budget approval. Twenty-five additional lessons/125 MCQs are isolated drafts with verifiable references and no fabricated human approval. Migrations 0009–0012 run only on new/disposable targets; original data and 0001–0008 remain unchanged. Previous presentation cleanup is not executed.

## 21 October 2026 — documentation consolidation and release hold

Archive the exact 12 retired documents before removal; consolidate active checklist and UI requirements into the retained roadmap/architecture. Edit only the approved 16 paths, keep 19 canonical Markdown documents and 211 release inputs, and preserve runtime code/tests/migrations/locks/data/media/credentials. No staging, commit, push, merge, migration, production change or history rewrite. Review the resulting diff/security findings before a separate commit approval. Ignore hardening must preserve safe templates, SQL source and public certificates.

The preceding GitHub audit distinguished a local unpublished release from older remote refs. No real .env/private data was tracked in inspected trees/history, but audited main still contained a retired development key. Ordinary future release updates do not purge history or recall external clones. External reuse/production rotation/history remediation remain separate owner decisions.

## 21 October 2026 — master Phase A and key retirement

The owner conditionally authorized the local baseline commit after security checks; it exists as 49407b2. Push consent was explicitly separate and never granted. Only the ignored development SECRET_KEY was rotated with 64 random bytes, private permissions and no fallback; production credentials/data/passwords were untouched. Old signatures/sessions intentionally fail; nine disposable checks verified their replacements. Known-value scanning supplements default Gitleaks rules, which missed the insecure development key. Do not restore that value from history or backup.

## 21 October 2026 — controlled cleanup and samples

Verify private full recovery/independent restore before cleanup. Archive isolated retired Express/Mongo and obsolete Python environment; retain active dependencies. Remove only proven unused starter/generated artifacts/imports and correct fabricated count fallbacks. Keep original/demo data/media, all migrations, historical evidence and dormant learner code. Public source/docs/IDE settings are trackable; private history/evidence/dumps stay out. A manifest export does not establish a published commit or production host.

Sample population uses a NEW isolated database and the exact original five-root/142-topic hierarchy; repeated/existing/symlinked destinations are refused. Select three existing leaves per subject, 15 original lessons/75 canonical questions, controlled tags and 30 normal reviewed links/relations. Never copy questions into subject pools or transfer real data. Engineering sample review/source checking is not independent academic/rights approval. No paid generation or new schema was introduced.

## 20 October 2026 — Phase 4B UI

Reuse existing tokens/components/router, one existing /search experience and one hierarchy request. Derive counts/numbering from full original API order, not filters/demo constants; render all roots and genuine loading/error/empty data. API subject buttons scroll/focus roots. Global expansion leaves individual native toggles functional. One bottom-right Tutor launcher preserves passage/citation/keyboard/mobile behavior; no RAG or learner activation. Current UI constraints are consolidated in ARCHITECTURE.

## 20 October 2026 — Phase 3 linking/discovery

Reuse Topic/TopicPublication/TopicRelation and canonical Question containers. KeywordLinkProposal owns evidence-bound phrase decisions; ConnectionScan owns queued derived plans. Analyze published text in editorial workflows only: Unicode whole-phrase, longest overlap, distinct targets/no self-links and eight-link limit. Withhold ambiguity and cross-formatting-node matches. Changed source needs fresh approval; identical analysis preserves decisions. No stored HTML rewrite/student-triggered matching.

Revalidate proposal/source/alias/target publication on reads; popup activation revalidates context, restores focus and opens safe local full-topic routes in a new tab. Related topics cap at six; tag publication is explicit/default false with stable slugs. Canonical topic/subject practice traverses eligible primary/related branches distinctly, paginates 50 and binds stateless grading to signed reviewed membership. No copied questions, saved attempts or new accounts. Migration 0008 is additive/reversible on isolated targets; real cutover is separate.

## 20 October 2026 — Phase 2 CMS and canonical metadata

Retain Django Admin/WYSIWYG instead of a React admin or duplicate Content model. Topic/ContentBlock/TopicPublication remain the draft/released unit; saving blocks or preparing PDFs cannot publish. Fix empty placeholder inlines rather than relaxing server sanitization. Tag/TopicAlias normalization and uniqueness, stable IDs/slugs and explicit review avoid ambiguous inferred links. Reuse TopicRelation review states and one canonical Question, primary/related/tag associations and existing quiz reviews. Legacy backfill preserves IDs/locations/fingerprints; new Admin associations require appropriate leaves. Migration 0007 preserves old records; reversal drops only new metadata and is not a production rollback approval.

## 20 October 2026 — Phase 1 superseding decisions

PostgreSQL became mandatory normal/production storage, superseding the earlier keep-SQLite-primary decision. Original SQLite remains an immutable archive; explicit isolated test/demos are allowed, never implicit fallback. Real migrations/transfer/sequence/native-restore proofs use disposable copies and preserve metadata/IDs/counters; real source freeze/cutover needs independent approval.

The content-first release superseded the earlier learner-enabled dashboard direction. All public student state/auth/report routes and UI activation are closed for every identity while Admin staff access remains. Retain nullable ownership schema, records and dormant code. Close raw private-media/unreviewed attachment serving; require explicit PDF text/rights approval. Budgets use conditional reservation and row-locked idempotent settlement; no live provider tests are implied.

## 19 October 2026 — retained foundation choices

Preserve React, Django/DRF and Django Admin rather than replacing the stack or adding a new CMS/vector/Redis service. Use explicit publication snapshots, one previous version, persistent quiz review fingerprints/stable IDs and deterministic stateless practice. Bounded immutable PDF candidates need text/rights review; no OCR or arbitrary remote fetch. Public prototypes/screenshots/synthetic fixtures do not certify real content or production operations. Migration 0005 integrated MVP tables; real database application was gated. The old student/dashboard and SQLite-primary directions are historical, superseded above.

Production content/language/rights coverage, approved model/rates/budget, target roles/TLS/media/durable recovery, hosting/domain and final release remain owner decisions. [Roadmap](IMPLEMENTATION_PLAN.md) and [handoff](AGENT_HANDOFF.md) contain the current next action.

## 23 October 2026 — explicit local authentication navigation

Hidden auth controls were caused by the running core.demo_settings backend correctly returning learner=false. Preserve that legacy boundary and select the existing ready student environment rather than bypassing it in React. Normal dev defaults closed; only explicit configuration enables students. A development-only API override avoids stale shell proxy values; production build/preview are unaffected. Use existing named Account menu without inventing a Profile route. Google remains disabled. No original-data migration, paid service or Git operation.

## 23 October2026 — PostgreSQL setup without cutover; deletion policy gate

Use existing Django models and migrations0001–0012. Preserve active student-review SQLite and originals; test only new loopback PostgreSQL databases from verified source copies. Separate generated migration/runtime/backup credentials; runtime DDL/sequence reset and backup writes denied. Use native exported-snapshot custom dump plus stable media, authenticated CMS AES-256-GCM and native independent restore. Do not enable production backup/scheduling/off-host services before owner configuration and acceptance. Retention is review-only; account deletion is readiness-only pending explicit owner approval of permanent erasure, session revocation, staff references, backup expiry and post-restore deletion ledger. Keep learner/AI/Google forced closed in unactivated staging/production profiles. Local PostgreSQL16.2 proof lacks SSL and does not establish PG17/production TLS or durable recovery. Daily dump nominal RPO24h requires owner decision on PITR.

## 23 October 2026 — commercial staging architecture

Choose a single-origin Render Python web service for React/Django/Admin with PostgreSQL17/private disk. Vercel browser access works, but Hobby cannot host this confirmed commercial/client product; avoid an extra paid frontend/proxy for the first staging environment. Preserve strict verify-full: Render internal self-signed TLS is incompatible, so test the external hostname with CA validation and restricted CIDRs before database use. Keep hosted learner/AI/Google closed and restrict staging access. Owner approved template restoration and30-day production retention requirement, not billing/Git publication/cutover.
