# Phase A conditional approval remediation — 21 October 2026

Protected the reviewed index/release/environment with a verified private checkpoint. Confirmed the historical Django key was used only by the scoped local development environment, then atomically rotated it without fallback or changing other environment fields/data. Verified nine session/signature/password/visitor/practice/quota impacts. Confirmed two historical commits contain the retired value and live GitHub main points to one; no history rewrite/push.

Downloaded/checksummed Gitleaks v8.30.1 outside application dependencies; staged/full-index/history scans reported zero findings. Independent known-value checks retain one retired historical-key finding and no current credential exposure. Reran 80 frontend tests/lint/build, 121 backend tests (four PostgreSQL skips), Django/migration and release/docs/Git checks. Updated authority/security/setup/status/testing/handoff for the approved local baseline commit. Application/models/migrations/locks, production secrets, databases/media remain unchanged; future push/cutover/deployment remain gated.

---

# Controlled cleanup and error diagnostics — 21 October 2026

Created and verified private recovery before changes. Archived retired Express/Mongo source/manifests and obsolete Python environment; removed unused starter SVGs and regenerable caches/Finder metadata/stale build output. Preserved active dependencies, original/demo data/media, migrations, historical evidence and dormant learner code.

Removed seven unused Python imports; corrected invented syllabus/search counts and added three regressions; sanitized credential-bearing screenshot capture. Added trackable workspace exclusions, explicit release-manifest/export tooling, release-aware document checks and CI coverage for docs/sample browsers. Canonical docs are no longer ignored; links to excluded archives are now labeled private references. Exact actual results and remaining blockers are in TESTING and AGENT_HANDOFF. No commit, push, deployment, real cutover or paid requests.

---

# Sample content population — 21 October 2026

Added a separate reproducible 142-topic/five-subject demo with 15 original lessons (6,754 note words), 75 reviewed sample MCQs/300 choices, 19 tags, 15 aliases, 30 reviewed relations/inline links and 30 publications. Added exclusive preparation, demo-only seeding, read-only verification, five backend tests and four corpus Chromium tests. Existing model/schema/frontend/provider implementations and earlier work remain intact. README and existing canonical docs include startup, catalogue, safety and review limits. Actual results are in TESTING; original SQLite and both earlier demos are unchanged. No Phase 5, cutover, paid calls, commit, push or deploy.

---

# Phase 4B — Targeted Frontend UI (20 October 2026)

Reused the existing React shell, tree, map, reader and themes. Added stable original-order hierarchy numbering, global/individual controls, API-root subject jump buttons and shared honest homepage/footer counts. Simplified the header to logo/Search/theme, removed redundant homepage filters/CTA and About footer navigation, compacted the map and preserved existing routes. Consolidated Tutor controls into one nonmodal launcher with Escape/close/focus return and bounded responsive content; corrected the unused third tablet reader column and tree text theme transition.

All Phase 1–3 rendering/discovery/learner boundaries remain; no backend or database migration commands, provider requests, package changes, Git publishing or deployment. Current actual results and corrected initial failures are in TESTING; exact Phase 4B files/next gate are in AGENT_HANDOFF. Phase 5 remains unapproved.

# Phase 3 — Dynamic Content Linking & Discovery (20 October 2026)

Added Admin Suggest Connections and individually reviewable phrase/context proposals, evidence-preserving regeneration, queued/fair scans and bounded derived link plans. Added safe accessible reader popups with fresh publication checks/new-tab actions, six related published topics, explicitly approved stable-slug tag pages and canonical topic/subject practice with signed stateless grading.

Retained existing Admin/content/MCQ models and learner containment. Migration 0008 adds only proposal/scan metadata, public-tag approval and lookup indexes; original SQLite/demo/old migrations remain untouched. No paid AI, real cutover, commit/push/deploy or Phase 4. Current commands/results, initial failures/corrections and limits are in [TESTING](TESTING.md); exact files are in [AGENT_HANDOFF](AGENT_HANDOFF.md).


# Phase 2 — Content Management Foundation (20 October 2026)

Implemented permission-filtered Topics/Content/Practice Questions navigation; retained WYSIWYG and source/resource controls; added submit-for-review state and draft-only standalone note saving. Fixed untouched empty rich-text inline rows blocking full-form saves; resource preparation now reports feedback.

Added controlled normalized Tag/TopicAlias registries, explicit draft/released tag associations, reviewed stable-ID TopicRelation edges, canonical Question primary/related/tag classification and distinct hierarchy collections. Existing review/grading remains stateless; legacy primary backfills keep existing approvals, while metadata changes require re-review. Reversible migration 0007 preserves original fields/IDs and SQLite high-water counters on copies. Learner features remain closed.

Actual verification, initial failures/corrections, unchanged source evidence and remaining limits: [TESTING](TESTING.md). Phase 1/P000–P003 evidence below remains historical and unchanged. No real migration, cutover, paid AI, commit, push or deployment. Next approved-scope boundary: stop before Phase 3 dynamic content linking and discovery.


# Changelog

## 2026-10-20 — Phase 1: content-first containment and PostgreSQL foundation

- Superseded the previous learner-enabled MVP and SQLite-primary scope; retained the historical entries below as prior claims, not current verification.
- Added explicit PostgreSQL configuration, a hash-pinned psycopg driver, isolated PostgreSQL test settings, real migration/transfer rehearsals and native restore verification. Original SQLite and migrations remain unchanged; cutover is not performed.
- Closed all public learner/authentication paths and student reports for every identity. Preserved administrative sessions, staff-account administration, public reading and reviewed stateless practice. React no longer mounts public student authentication/forms or probes learner state.
- Preserved existing Admin editor/tree/templates; separated PDF preparation from explicit approval/publication. Removed unconditional private-media serving and withheld raw historical attachment links without deleting records/files.
- Added PostgreSQL quota/settlement concurrency coverage and a row lock for idempotent settlement. Corrected a streaming-response test that had closed PostgreSQL's test connection; updated stale browser selectors to match existing UI.
- Protected the preexisting worktree and verified source SQLite backup/recovery before changes. Current results, file inventory, first-run failures and limitations are in Phase 1 evidence (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).


## 2026-10-19 — PREPAL 1.0: Final UI/UX Refinement, Search Fix, Authentication & Student Dashboard

- **Search Overhaul & Typo Tolerance**:
  - Diagnosed root cause: search had previously searched only published study blocks and had strict keyword filtering, causing searches like `palaeothic` to yield zero results even though syllabus topics exist.
  - Overhauled `content/services/search.py` to index all 152 discoverable topics, verified notes, and approved PDFs.
  - Implemented case-insensitive partial word matching, normalized whitespace, and `difflib`-based typo suggestions (`palaeothic` → `palaeolithic`).
  - Draft note bodies and private PDFs remain completely protected and inaccessible.
- **Consistent Curriculum Topic Counts (152 Topics across 5 Streams)**:
  - Diagnosed and resolved 142 vs 152 discrepancy: 142 was the core seed from `syllabus_142.json`; 10 foundational methodology topics bring DB total to 152 across 5 streams.
  - Unified all UI and API counts to 152.
  - Added prominent summary statistic pills above the syllabus list on the homepage and `/syllabus`.
- **Simplified Navigation & Coherent Brand**:
  - Removed duplicate navbar search input, Full Syllabus link, and multi-palette dropdown selector.
  - Clean, compact navbar layout: `Prepal Logo | Syllabus | Search | About | Sun/Moon Toggle | Login / Sign Up` (or user profile menu with Dashboard and Logout when authenticated).
  - Consolidated to single coherent brand identity: clean Light mode (default) and comfortable Dark mode.
  - Replaced oversized theme controls with a compact sun/moon toggle button.
- **Rajasthan Visual Identity on Homepage Hero**:
  - Replaced generic right-hand block with an elegant, recognizable vector map of Rajasthan (`RajasthanMap.jsx`) highlighting Ajmer (RPSC HQ), Jaipur, Jodhpur, Bikaner, Udaipur, Kota, and the Aravalli range.
  - Subtle entrance animation respecting `prefers-reduced-motion`.
- **Student Authentication & Ownership (P002 Resolved Safely)**:
  - Implemented built-in Django session auth: registration, login, logout, and session status endpoints.
  - Added `user` ForeignKey to `Bookmark`, `UserProgress`, and `QuizAttempt` models with conditional uniqueness constraints (`Q(user__isnull=False)`).
  - Created additive migration `0006_learner_ownership.py` and validated on isolated `.local/demo/demo.sqlite3`.
  - Completely isolated legacy ownerless records (`user=None`); ensured zero cross-user data leakage.
- **Student Dashboard & Progress Tracking**:
  - Created `/dashboard`: welcome section, syllabus progress percentage, total completed topics, saved bookmarks, practice test performance history, and suggested next topics.
  - Added interactive Bookmark and Mark Completed controls in the study workspace (`/topic/:slug`) with immediate feedback.
- **Full Verification Suite Passed (100% Green)**:
  - 62/62 Django backend tests passing.
  - 59/59 Vitest frontend tests passing.
  - 8/8 Playwright E2E browser tests passing.
  - `npm run check` (ESLint, Vitest, Vite production build) passing cleanly (0 errors, 0 warnings).
  - 27 browser-rendered screenshots captured and documented in `docs/design/GALLERY.md`.
- **Database Safety Intact**: Real database `backend/db.sqlite3` remains untouched (SHA-256 `035bb88637e77ff361dab75c0d4cf80db0a6220f270870a18929be2c3ba313e4`).

---

## 2026-10-19 — Urgent syllabus hierarchy restoration & academic UI redesign

- **Complete Syllabus Hierarchy Restored:** Diagnosed the regression where topics without published snapshots responded with 404 and disappeared from the syllabus tree. Extracted all 142 official RPSC curriculum topics into fixtures, implemented `get_syllabus_tree()` in publication services, and added safe fallback in `/api/topic/<slug>/` returning coming-soon metadata and subtopics without exposing unpublished drafts.
- **Academic UI Overhaul & 3 Reversible Palettes:** Eliminated the unpopular green/teal SaaS theme. Replaced it with an editorial monograph study aesthetic and an interactive palette switcher supporting 3 distinct directions (Oxford Academic, Minimalist Monograph, Scholarly Research) with tailored dark modes.

---

## 2026-10-19 — Autonomous local MVP implementation

- Implemented the responsive light/dark library, syllabus, study/tutor, search, PDF, practice/results and help/error interfaces; original prototype and 35 real screenshots accompany the code. Added reviewed publication snapshots, related topics, staff previews, private PDF processing/review, published-only search, bounded RAG/provider/citation/budget services and stateless reviewed practice.
