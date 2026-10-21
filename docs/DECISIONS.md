# Phase A conditional approval and key retirement — 21 October 2026

The owner authorized the named local baseline commit once exposed-key remediation and checks pass. Confirmed a development-only environment; only SECRET_KEY reused the exposed value. Replaced it with an independent 64-random-byte URL-safe key, atomically, with mode 0600; other environment fields are unchanged. Do not retain the exposed key in SECRET_KEY_FALLBACKS. Existing sessions/reset links/cookies/practice tokens intentionally become invalid; data/passwords remain intact. No production configuration was accessed.

The key remains in two old commits, one confirmed as GitHub main via read-only SSH. Removing it would rewrite history and is not authorized or required for retiring this known local credential. No other active credential was found in scanned staged/history inputs. External reuse/remote visibility cannot be established from this workspace; future production secrets must be independently generated. Separate push/production gates remain. GitHub CLI lacks login, but SSH ref reads succeed. No remote refs were modified.

---

# Controlled cleanup decisions — 21 October 2026

- Verify a complete private snapshot before cleanup, including ignored canonical documentation; keep Git index/HEAD/remotes unchanged.
- Archive obsolete environment and retired Express/Mongo files outside the checkout after process/reference/isolation checks. Retain active dependencies.
- Preserve all original/demo data/media, migrations and historical evidence; no deduplication of referenced attachments or dormant learner-code retirement.
- Replace invented syllabus/search totals with actual available data and honest unavailable states; preserve filtering and original-order routing.
- Track sanitized canonical docs and workspace settings. Keep historical evidence private; public docs identify archives without broken links to excluded files.
- Export an explicit hash-verified release copy for clean dependency installation/testing, with no commit or production data. Remote CI and production rollout remain separate evidence.
- Report PDF timeout policy, live Gemini evaluation and topic PDF export as remaining scope/production questions, without implementing Phase 5.

---

# Sample-content decisions — 21 October 2026

- Use a new isolated `.local/sample-content-v1` database rather than altering either existing demo. Repeat preparation refuses existing destinations and preserves edits.
- Preserve the exact 142-topic fixture, verified equal to the original SQLite hierarchy. Select three existing leaves per root; publish only lessons and necessary navigation ancestors.
- Keep 15 canonical quiz containers and 75 primary-topic questions. Derive subject membership from existing ancestry; no copied subject questions or schema changes.
- Reuse 19 controlled tags across lessons. Approve 30 curated existing-model links/edges through normal services, keeping source HTML untouched.
- Mark all material and review records as development samples. Reference checking is not independent human academic approval. No paid generation, external copied notes, source transfer or Phase 5 work.

---

# Phase 4B decisions — 20 October 2026

- Owner approved the Phase 4A frontend map and resolved its interaction choices in the Phase 4B brief. No backend changes/migrations, paid AI, learner activation, Git publishing or deployment. Stop before Phase 5.
- Keep existing components, router and tokens. Search links to `/search`; no duplicate search. Remove only header Syllabus/About links, retaining their routes and footer syllabus/help navigation.
- Share one hierarchy request per AppShell mount; derive homepage/footer totals from returned roots and all descendants. Loading/error states do not substitute zero or demo figures. Render all actual API roots without truncating synthetic/future roots to five.
- Preserve original hierarchy positions for filtered numbering. Root/child/deeper formats are numeric/dotted/alphabetic; alphabetic sequences restart per parent. Keep title text/slug navigation unchanged.
- Homepage subject buttons scroll and focus matching roots, without filtering or navigating away. Expand/collapse controls remain compatible with subsequent individual native-summary toggles.
- Keep exactly one bottom-right Tutor launcher. Remove toolbar/mobile Tutor controls; keep passage explanation, keyboard close/focus return, citations and current chat API behavior. This phase does not change RAG or provider configuration.
- Phase 3 tests and backend/migration results below remain historical evidence; current Phase 4B checks and limitations are in TESTING. No Phase 5 scope is inferred.

# Historical Phase 3 decisions — 20 October 2026

- Owner approved dynamic linking/discovery and canonical practice, superseding Phase 2 discovery exclusions. Stop before Phase 4; its scope/acceptance criteria and approval have not been supplied.
- Reuse Topic/TopicPublication, TopicRelation, Tag/TopicAlias and canonical Question associations. New KeywordLinkProposal is an evidence-bound phrase decision, not a duplicate general Topic relationship. ConnectionScan owns queued analysis and a bounded derived render plan.
- Analyze only published article text in editorial workflows. Normalize NFKC/casefold/whitespace, use whole-phrase boundaries, prefer longest overlaps, suppress repeated targets/self-links and cap at eight. Do not rewrite HTML. Preserve all evidence/decisions; changed HTML requires fresh review.
- Withhold ambiguous terms and phrases spanning separate formatting nodes rather than invent mappings or flatten educational formatting. Rejecting an inline phrase does not revoke published syllabus associations.
- Tag public approval is explicit/default false; released M2M associations and immutable slugs govern public pages. Current approved hierarchy/relations drive six related topics without a stale relationship cache.
- Store preselected link spans, then live-check every mutable boundary. Revalidate popup context at activation; use safe React text, keyboard focus controls and local new-tab routes. No constant polling or student-triggered regeneration.
- Retain existing quiz review containers and shared stateless grading. Collections reference canonical IDs, traverse published primary/related branches, paginate 50 questions and bind checking to keyed signed manifests. No new attempts/accounts or advanced quiz assembly.
- New migration 0008 is additive/reversible on disposable databases. Real cutover, paid AI/infrastructure, commit/push/deploy and Phase 4 remain unauthorized.


# Phase 2 decisions — 20 October 2026

- Owner approved the content-management foundation, superseding the previous stop-before-Phase-2 instruction only for this scope. Stop before **Phase 3 dynamic content linking and discovery**.
- Reuse Topic + ContentBlock + TopicPublication as the notes publication unit. Draft/released tag M2Ms express editing versus approval without adding a duplicate Content model.
- Tag and TopicAlias names are globally unique after NFKC/whitespace/casefold normalization. Ambiguous aliases are rejected rather than mapped to multiple topics. Registry administration remains explicit; no inferred links/tags or search expansion.
- Reuse TopicRelation stable-ID edges with review status. Matching existing reviewed edges retain approval; no unreviewed stored edge is silently approved.
- Retain one canonical Question and its legacy quiz/review container. Hierarchy collections query primary/related associations distinctly; no question copying or advanced quiz assembly. Backfill preserves old primary locations and fingerprints; new/moved Admin associations use leaves.
- Migration 0007 is additive/reversible and tested on disposable PostgreSQL/SQLite. Reversal preserves legacy records but removes Phase 2 metadata; real source/cutover remains gated. Original 0001–0006 and SQLite data stay untouched.
- Keep the existing editor. Fix its empty-placeholder inline submission bug and remove standalone block auto-publication because both violate the requested safe editorial workflow.
- No paid services, commit/push/deploy, student release, homepage redesign, Tutor feature or Phase 3 discovery work was authorized/performed.


# Current decisions

## 20 October 2026 — Phase 1 superseding decisions

- The owner now requires PostgreSQL as primary. This supersedes the earlier keep-SQLite decision below; SQLite remains an untouched source archive and explicit isolated test/demo backend.
- The approved release is content-first. The 19 October student authentication/dashboard promotion recorded in CHANGELOG is superseded. All learner APIs, UI activation and Admin reports are closed for every identity; models/data remain retained. Administrative staff authentication remains functional.
- Original migrations 0001–0006 are unchanged. Pending 0005/0006 run on a disposable SQLite copy; a new PostgreSQL database genuinely executes its schema migrations before transfer. Source migration-recorder IDs/dates are imported only after graph equality is checked; target execution history is also retained in the private manifest.
- Only a fresh local rehearsal database can be populated by the prepared transfer tool. Real cutover, credentials, hosting, paid AI, commits/pushes and Phase 2 remain gated. Native PostgreSQL backup/restore is the rollback path; current code must not fall back to the unmigrated original SQLite archive.
- Existing WYSIWYG/tree/editor templates are preserved. PDF extraction no longer automatically approves or republishes; raw private-media serving and unreviewed legacy attachment links are closed to enforce the existing publication boundary.
- Tracked/nonignored pre-Phase1 files are recoverable from baseline Git HEAD `ee272a6` plus the private protected worktree archive for uncommitted additions. Local ignored scope documents were intentionally updated; their superseded decisions remain explicitly recorded here and in the unchanged historical changelog entries. Historical evidence and the earlier changelog are retained. Current proof is Phase 1 verification (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).

## Earlier decisions (historical; superseded where stated above)

- Final autonomous directive supersedes earlier planning-only and per-batch stops for ordinary local MVP work. Real migrations, destructive actions, spend, Git publishing and deployment remain gated.
- Preserve React, Django/DRF, Django Admin and SQLite; no MERN/vector/Redis/new admin SPA.
- Guest reading/search and **stateless** reviewed practice are implemented. P002 legacy learner paths stay closed. Guest AI remains default-off until approved configuration/cap.
- Explicit publication snapshots separate draft editing from every public consumer. One previous publication is retained; no complex revision CMS.
- Persisted quiz review fingerprints replace the temporary ID allowlist. Changed content requires re-review; stable IDs/revision tokens bind checking to preview.
- Private immutable PDF candidates require bounded extraction, text/rights review and explicit topic publication. No OCR or arbitrary remote fetch.
- Original HTML prototype precedes implementation; final screenshots are browser renders. Synthetic content and mocked AI are labeled.
- One additive migration 0005 integrates MVP tables; old migrations and existing records are preserved. Applied only to isolated demos/restored copies.
- Production AI model/prices/cap, real content/language coverage, host/domain/backup retention and public deployment are unresolved owner decisions. No invented approvals.

Earlier reasoning and all prior decisions remain in history (retained privately as `docs/history/2026-10-19-before-execution/DECISIONS.md`).
