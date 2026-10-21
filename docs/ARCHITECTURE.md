# Release/workspace boundary after controlled cleanup

The application architecture remains React/Vite plus Django/DRF/Admin with PostgreSQL as the normal database. Cleanup changes only imports, honest syllabus/search counts, capture tooling, workspace visibility and release validation. Syllabus statistics use the original returned hierarchy, including genuine zero values and loading/error states. Search makes no invented corpus-size claim. Learner implementations remain dormant and unchanged.

`prepal.code-workspace` and `.vscode/settings.json` expose the application folder while excluding dependencies/generated/private runtime trees. `scripts/release_manifest.py` defines hash-verified source/test/config/canonical-document inputs and excludes runtime data, private archives and generated files. CI checks this boundary and release documentation; it also prepares a separate academic sample for its browser suite. Existing history/evidence remains private, unchanged and recoverable. Local release-copy success does not establish remote CI or production hosting.

---

# Isolated academic sample-data tooling

This batch adds no application architecture, model, route or frontend behavior changes. `scripts/prepare_sample_demo.py` creates a new private destination with an explicit marker and invokes existing migrations under `core.demo_settings`. `create_sample_content` reads the versioned notes/MCQs and canonical syllabus fixtures, validates leaf membership and counts, and uses existing publication/quiz/connections services. Controlled tag reuse and primary-topic ancestry drive the unchanged public tag and canonical practice services. No seed runs automatically during server startup or a public request.

The prepared sample database is `.local/sample-content-v1/demo.sqlite3`; original SQLite and earlier demos are preserved. `verify_sample_demo.py` turns on SQLite query-only protection before ORM and API checks. The separate Playwright sample configuration reuses loopback Django/Vite orchestration without modifying the legacy integration corpus. All AI remains mock-only in demo settings.

---

# Phase 4B frontend UI architecture

AppShell owns one `/topics/?tree=1` useResource request and provides SyllabusContext. useSyllabus shares its data/loading/error/retry with Home, SyllabusPage and TopicPage; the footer derives counts from the same response. No persisted client state, new backend endpoint or additional search system is added. Statistics show a loading/error message, never fabricated fallback counts.

indexSyllabus builds stable numbering paths from the full API order. SyllabusTree accepts originalTopics for filtered callers; numbering never derives from the filtered sibling index. Roots use 1–5 for the original five-subject corpus, immediate children use 1.1/1.2, deeper levels restart A/B/C within each parent (AA follows Z). Explicit expansion sets drive native details/summary elements. Individual toggles remain available after either global action; Collapse All closes descendants while preserving root labels. The homepage's API-derived buttons scroll/focus the corresponding root without filtering the corpus or changing routes.

The shell keeps logo/Search/theme controls at every viewport, retains footer syllabus/search/help routes and has no student navigation. A single nonmodal bottom-right Tutor panel supports close/Escape and launcher focus restoration without scrolling; passage helpers and all API payloads remain. Desktop/tablet retain two reader columns. Phase 3 annotation, popup, tag, related-topic and collection implementations are unchanged. No backend/schema/migration/auth/publication/RAG changes occur in Phase 4B.

# Phase 3 current discovery architecture

The modular React/Django/Admin foundation below remains. Phase 3 supersedes its earlier discovery deferrals; no CMS or Question model is replaced.

- `KeywordLinkProposal` stores source/target Topic FKs, normalized phrase, context, UTF-16 text-node spans, source HTML digest/revision and pending/approved/rejected decisions with reviewer/time. Unique source/target/phrase/hash preserves repeated decisions. Changed HTML creates new pending evidence; old decisions remain historical.
- `ConnectionScan` is one-to-one with TopicPublication. It stores queue state/age, revision/hash and at most eight preselected approved occurrences. Admin-only trie matching uses NFKC/casefold/whole-phrase boundaries, longest overlap resolution, distinct targets and no self-link. Existing anchors, headings and code are excluded. Matching is within one text node, preserving formatted markup.
- Publication/restore prioritizes its own scan and queues vocabulary-dependent articles. Alias save/delete queues scans; Admin saves process a bounded batch. A fair oldest-analysis-first queue is drained with `regenerate_connections`. Suggestions and approvals recompute link plans. Student GET never matches article text or computes plans; it reads stored spans and live-checks revision/hash, proposal approval, unambiguous title/approved alias and target/ancestor publication. Withdrawals fail closed immediately on the next request.
- SafeHtml sanitizes the source first, then adds trusted local anchors using DOM APIs after exact text/offset checks. Authored data attributes cannot forge controls. React popups revalidate a no-store context endpoint before showing published descriptions or a new-tab action. Focus is trapped/restored without scrolling; Escape, close and outside dismissal work on desktop/mobile. Neither database HTML nor snapshots are rewritten for linking.
- Related content uses approved snapshot TopicRelation edges plus current published child/sibling/parent associations, uniquely capped at six. Rejecting a phrase does not revoke an independently published syllabus relationship.
- Tag.is_public defaults false; existing tags are not auto-approved. Published tag M2Ms drive paginated public pages with syllabus paths and estimated reading time. Stable tag slugs cannot be changed by normal saves.
- Public syllabus practice traverses visible branches and canonical primary/related question associations. Indexed candidate quiz queries and prefetches avoid N+1 reads; entire matching quiz reviews are fingerprint-validated in memory. Fifty-question pages use signed, keyed manifests and shared deterministic grading. No Quiz/Question copy, attempt or learner identity is created. Large-corpus load benchmarking remains pending.

No shared process cache is used. Database plans are source-bound and every mutable public eligibility boundary is rechecked. Important indexes cover proposal source/status/revision, alias status/topic, pending scan age and tag approval; existing FK/M2M indexes serve hierarchy/question/tag joins. Current publication resolution remains bounded to 5,000 entries; this is an MVP bound, not a large-corpus scale claim.


# Implemented Architecture — PREPAL 1.0

## 1. System Topology & Technology Stack
- **Frontend**: React 19 (SPA) with Vite. Modular architecture with lazy-loaded routes and PDF worker chunks. Vanilla CSS design system with CSS custom properties (`tokens.css`, `App.css`). No heavy component or animation frameworks.
- **Backend**: Django 6 on Python 3.14 with Django REST Framework. PostgreSQL is the default application backend (psycopg 3); SQLite is explicitly isolated for source archives, demos and fast tests. There is no SQLite production fallback.
- **Development & Production Proxies**: In development, Vite proxies `/api` to Django loopback (`127.0.0.1:8000`). In production, Nginx or Cloudflare serves static assets from `dist/` and forwards `/api`, `/admin`, and `/static` to Gunicorn/Uvicorn.
- **State & Session Persistence**: Authentication uses Django's secure, HTTP-only session cookies (`sessionid` and `csrftoken`). No auth tokens are stored in browser `localStorage`. Theme preference (`light`/`dark`) is the only state persisted client-side.

## 2. Content-first release and administrative identity
- Public student registration/login/logout/status, dashboards, bookmarks, progress, saved attempts and reports are disabled for every identity at URL registration, independently of settings.
- Learner models, nullable user fields, constraints and historical rows remain stored for a later approved release. Public reading responses never query their status.
- Django Admin retains normal staff authentication and editorial permissions. Only superusers can manage staff accounts; learner reports and nonstaff account details are closed.
- React does not mount student authentication or expose its forms. Legacy login/signup/dashboard URLs show an unavailable notice. Stateless practice remains available with CSRF.

## 3. Search Engine Architecture
- **Bounded Database Search (`content/services/search.py`)**:
  - Searches the configured discoverable syllabus topics (142 original / 152 synthetic demo), verified notes, and approved PDFs.
  - Normalizes whitespace and executes case-insensitive partial word queries.
  - Generates typo tolerance suggestions using Python's standard `difflib.get_close_matches(word, vocabulary, cutoff=0.72)`.
  - Draft note bodies and unapproved PDFs are strictly excluded from search querysets.

## 4. Retained learner schema
Ownership migration 0006 remains in the schema and is exercised on isolated copies/PostgreSQL. It does not enable a product feature. Historical handlers/components are dormant; their release requires a separate approved phase. The earlier student-dashboard release decision is superseded in [decisions](DECISIONS.md).

## 5. RAG & AI Tutor Safety Controls
- **Scoped Retrieval**: `DatabaseRetrievalProvider` retrieves only the current lesson text, approved PDF pages, and up to two explicitly linked prerequisite/connected topics with opt-in.
- **Budget & Quota Reservations**: Pre-allocated spend caps and per-session rate limits prevent runaway API billing.
- **Answer Integrity**: Real source citations are validated against a server manifest; invalid or out-of-scope citations fail closed.

## 6. Schema Migrations & Isolation
The original SQLite database remains at content migration 0004 and is blocked as an application runtime path. A read-only backup is restored to a new copy; real migrations 0005–0008 execute there. A new local PostgreSQL target independently executes the same graph. Concrete fields and explicit M2M rows are transferred with IDs/timestamps/migration history preserved, then hashes, foreign keys and identity high-water marks are verified. PostgreSQL dump/restore is independently checked. No original migration file or source database was modified; real cutover awaits approval. See [database](DATABASE_SCHEMA.md) and evidence (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).

## 7. Content Management Foundation (Phase 2)

Django Admin has three permission-filtered primary sections: **Topics**, **Content**, **Practice Questions**. Superusers retain advanced maintenance and staff-account tools. ResourcePage is read-only and superuser-only; direct QuizReview maintenance is superuser-only. Editors use the existing Topic preview/publish and Quiz review workflows with their assigned model permissions.

Topic remains both a syllabus node and the primary location for its ordered ContentBlocks/resources. TopicPublication remains the released notes bundle, avoiding a duplicate Content model. Topic.tags is draft metadata; TopicPublication.tags and snapshot tag IDs/names/slugs are synchronized only during explicit publish/restore. Saving either inline or standalone notes cannot publish. Editorial draft/in_review state supports review queues; explicit publication is the approval boundary. One previous publication is retained.

Tag normalizes names with Unicode NFKC, collapsed whitespace and casefold, with database uniqueness on normalized names and slugs. Renames retain stable slugs; normal saves reject slug changes. TopicAlias maps one globally unique normalized keyword to a Topic FK and starts draft; approved/withdrawn are explicit editorial states. Approved aliases now feed Phase 3 phrase proposals; general search ranking and the Tutor are unchanged. TopicRelation reuses the existing stable Topic FKs and related/prerequisite kinds, with draft/approved/withdrawn status. Only approved edges enter new snapshots; central publication resolution suppresses revoked edges for existing consumers without adding Tutor functionality.

Question is the canonical question record, retaining its original quiz/review container. A required primary_topic FK and optional related_topics/tags M2Ms add academic classification. Admin requires leaf subtopics for new/moved associations and rejects repeating the primary as related. Legacy primary locations are backfilled from quiz.topic without changing any original field or PK; existing ancestor-level locations remain editable. Read-only subject collections traverse the existing hierarchy and use distinct question IDs rather than copying questions or creating new quizzes. The Admin collection filter includes drafts; the service's default reviewed mode requires current publication and a matching quiz review. Question metadata changes invalidate reviews/tokens; legacy default backfills retain their original fingerprints.

The existing WYSIWYG and paste sanitizer are retained. Empty placeholder HTML is submitted as an empty value, preventing untouched extra inlines from blocking saves. Server nh3 publication/preview sanitization and browser SafeHtml/Markdown boundaries remain. Phase 3 public context/tag/practice routes extend this foundation; see API_DOCUMENTATION.
