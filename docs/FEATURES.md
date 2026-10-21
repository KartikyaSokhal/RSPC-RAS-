# Content-first feature inventory

The current implementation is local commit 49407b2 plus uncommitted documentation/ignore cleanup. This batch changes no application behavior. Verification below refers to tests and prior named batches, not production usage; [TESTING](TESTING.md) gives actual results and limits.

| Area | Implemented behavior | Important limit |
|---|---|---|
| Reading/navigation | Published snapshots/notes, breadcrumbs, original-order numbered expandable syllabus and subject jump controls | Preserve all actual API roots/slugs; unavailable data never invents counts |
| Shell/themes | Existing Search/theme header, compact Rajasthan map hero, branded footer and shared dynamic statistics | No active student/auth navigation; light/dark/reduced-motion tokens retained |
| Admin/editor | Topics/Content/Practice Questions, WYSIWYG, draft/review/private preview/explicit publish/withdraw, draft-only saves | Maintenance/staff management permission-restricted; saving/extracting never auto-publishes |
| Controlled metadata | Normalized tags/aliases and stable-ID reviewed relationships; primary/related MCQ associations | Tags/aliases/edges require appropriate approval; stable slugs/IDs preserved |
| Dynamic discovery | Evidence-bound approved phrase links/popups, six related topics and approved tag pages | Admin-only matching, source-bound decisions and live withdrawal checks; stored HTML unchanged |
| Practice | Reviewed stable quiz IDs and deduplicated topic/subject/child collections, 50-question pages and signed stateless checking | No question copies or saved attempts; changed review/membership invalidates preview tokens |
| Search | Eligible topic titles, published notes and reviewed PDFs with bounded typo suggestions | No private/draft body exposure or production-scale performance claim |
| Uploaded PDFs/images | Bounded PDF preparation, explicit text/rights review, approved file delivery and PDF.js/text fallback | No OCR; raw private-media/legacy attachment URLs withheld; no topic-note PDF export |
| Rendering | Server sanitizer, DOMPurify educational HTML and raw-HTML-disabled AI Markdown | Active markup blocked; publication/file eligibility independently enforced |
| Existing Tutor | Selection/source citations, bounded current/optional-reviewed-related retrieval, quotas/cost reservations and mock adapter | Live mode defaults off; strict current-topic-only scope and live quality remain pending |
| Learner containment | All student auth/profile/dashboard/bookmark/progress/attempt/report routes unavailable for every identity | Admin staff login remains; dormant schema/data preserved |
| Database/recovery | PostgreSQL default, preserved schema through 0008, disposable transfer/sequence/native-restore tooling | No real cutover, durable off-host recovery or production operations established |
| Academic sample | Separate 142-topic/five-subject demo, 15 lessons/75 MCQs, 19 tags/15 aliases/30 approved links and relations | Non-production originals; engineering review is not human editorial/rights approval |

No live Gemini, production host/domain, staged deployment, current-topic PDF export or completed master Phase C claim. [Scope](MVP_SCOPE.md), [architecture/UI constraints](ARCHITECTURE.md), [workflow](ADMIN_WORKFLOW.md) and [roadmap](IMPLEMENTATION_PLAN.md) define what stays enabled/deferred. Historical attachments, data, media, locks, migrations and learner implementations remain stored and unchanged.
