# Phase A remediated release baseline — 21 October 2026

No application feature changes during Git preparation/key remediation. Existing syllabus/CMS/publication/discovery/stateless practice, uploaded-PDF reading, safe rendering and learner containment remain. Only local development credentials rotate; users of that normal development environment must reauthenticate/reload signed practice after rotation. Explicit synthetic demo/test keys are independent and unchanged. Topic-note PDF export and strict current-topic Tutor remain pending Phase C; current optional related-topic retrieval is not that stricter feature. No live Gemini or production deployment/cutover validation is claimed.

---

# Cleanup additions

Syllabus statistics now reflect available hierarchy data without 152/10/five-stream fallbacks; genuine zero notes remain zero. Loading and errors withhold totals and disable status-count actions until data is available. Search uses count-free published-material wording. Three focused frontend regressions cover loading/failure/empty data and filtering against original totals.

Workspace exclusions, sanitized demo-only Admin capture, canonical-document tracking and explicit private-data-free release exports are operational improvements. They add no learner feature, AI capability, content publication or PDF export. Live Gemini and topic-to-PDF export remain unverified/unimplemented respectively.

---

# Content-first feature inventory

| Area | Current release behavior | Verification boundary |
|---|---|---|
| Academic sample corpus | 15 existing leaf lessons across five subjects; 75 four-option MCQs, 19 tags and 30 reviewed links in a separate demo | Agent source review for development only; 97 read-only HTTP checks and Chromium corpus coverage; human editorial release review pending |
| Reading/navigation | Full numbered syllabus outline; Expand All/Collapse All and individual toggles; original positions under filters; subject jump buttons | Synthetic UI/browser coverage; original data/slugs retained |
| Frontend shell | Logo/Search/theme header, compact map hero, dynamic subject/topic statistics and retained footer branding | Shared hierarchy response; loading/errors do not invent counts; existing search route reused |
| Topic reader | Published snapshots, notes, breadcrumbs and related lessons; one responsive bottom-right Tutor launcher with Escape/close/focus return | Existing safe rendering/Phase 3 discovery retained; learner controls remain disabled |
| Admin | Topics/Content/Practice Questions, retained WYSIWYG, draft/review/preview/explicit publication/withdrawal; draft-only saves and PDF feedback | Backend and Chromium Admin workflows; maintenance restricted |
| Content discovery | Reviewed phrase links and revalidated accessible popups; six related published topics; approved tag pages | Admin-bound analysis, preserved decisions, source-bound plans, live withdrawal checks; no stored HTML rewrite |
| Editorial registry | Controlled tags/aliases, stable slugs/IDs, draft/released M2Ms and explicit tag public approval | Existing tags default private; draft/withdrawn content excluded |
| Dynamic MCQ practice | Canonical topic/subject/child-branch collections, deduplicated 50-question pages, stateless checking | Current quiz reviews/publication required; signed manifests reject changed or mismatched answers |
| PDFs | Bounded preparation, explicit review/approval, published resource serving, PDF.js/text fallback | Synthetic and hostile fixtures; no OCR/live corpus review |
| Search | Discoverable topic titles plus eligible published notes/reviewed PDFs | API/browser tests; no production load claim |
| Practice | Fingerprinted reviews, stable IDs, signed revisions, deterministic stateless checking | Repeated grading creates no attempts for any identity |
| Learner features | All student authentication/profile, dashboard, bookmarks, progress, saved attempts and reports disabled | Direct API requests fail closed without queries; staff/administrative login remains functional |
| Rendering | DOMPurify educational HTML; Markdown raw HTML disabled; server publication sanitizer | Existing rendering-security regressions retained |
| AI | Bounded current/related-source retrieval, selected text, quotas and citation checks | Mock provider only; live AI remains default-off and unverified |
| PostgreSQL | Default configuration, real schema migrations, ID-preserving transfer, sequence verification | Disposable loopback target; original SQLite unchanged; real cutover pending |
| Recovery | Private SQLite backup/restore and native PostgreSQL dump/restore rehearsal | Local proof; no durable off-host retention or production recovery SLA |

Legacy ContentBlock attachments remain stored but their raw public URLs are withheld. PDFs must use reviewed LearningResource routes. Public private-media routing is closed. Existing published images retain their hash-checked route.

Current results and compatibility: [TESTING](TESTING.md). Historical command results: Phase 1 verification (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`). Earlier implementation evidence (retained privately as `docs/evidence/MVP_IMPLEMENTATION_VERIFICATION.md`) is historical and does not describe the current release gate.
