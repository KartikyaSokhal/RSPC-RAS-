# Architecture

Prepal is a React 19/Vite SPA plus Django 6/DRF, Django Admin and PostgreSQL. Source structure remains unchanged by documentation cleanup. [Database schema](DATABASE_SCHEMA.md), [API](API_DOCUMENTATION.md), [Admin workflow](ADMIN_WORKFLOW.md) and [AI system](AI_SYSTEM.md) describe their detailed boundaries.

## Runtime and identity

Vite proxies same-origin /api to private Django during local development. Reviewed Nginx/systemd/Gunicorn examples live under deploy/ and backend/gunicorn.conf.py; they are not an installed/verified production service. Static output and private media are separate. No retired Express/Mongo launch path remains active.

Django sessions provide administrative identity with HTTP-only cookies. Only superusers manage staff accounts. Public learner auth/dashboard/bookmark/progress/attempt/report URLs are fixed unavailable handlers for every identity; retained models/nullable ownership constraints and historical rows do not enable student features. Public serializers do not read global learner state. Stateless practice uses CSRF and signed manifests, not saved attempts. Theme preference is the only persistent student UI state; no auth token is stored in localStorage.

## Content and publication

Topic is a stable syllabus node and primary location for ordered ContentBlocks/resources. TopicPublication is the released bundle, with one previous snapshot; no duplicate Content model or general revision CMS. Draft/in_review state supports editing/review. Only explicit publication/restore synchronizes snapshot text, references, resources and tag M2Ms. Inline/standalone note saves cannot publish. PDF extraction creates review candidates, never automatic approval/publication. Raw legacy attachment URLs are withheld; approved images/resources use eligibility/hash-checked handlers.

Tag/TopicAlias normalize NFKC, collapsed whitespace and casefold names with database uniqueness. Tag slugs remain stable; public tag approval defaults false. Aliases map to existing Topic IDs and start draft. TopicRelation reuses stable source/target FKs and related/prerequisite kinds with explicit review status. Public resolution suppresses withdrawn/unapproved edges, including those in old snapshots.

Question is canonical within its existing quiz/review container. One primary topic plus optional related topics/tags provide classification; Admin validates leaf associations and primary/related overlap. Legacy backfill preserves IDs/original locations/fingerprints. Subject/topic collections traverse eligible hierarchy branches and distinct question IDs, never copy questions or create quizzes. Review fingerprints invalidate on meaningful question/classification changes. The draft-inclusive Admin collection view is not a public retrieval service.

## Approved discovery and safe rendering

KeywordLinkProposal records source/target IDs, normalized phrase/context, HTML hash/revision, UTF-16 spans and reviewer decisions. Reanalysis preserves identical evidence decisions; changed HTML requires fresh review. ConnectionScan stores a queued derived plan, not a duplicate relationship model. Admin/management matching uses whole-phrase Unicode normalization, longest overlap, distinct targets, no self-link and eight-link cap. Existing links/headings/code are excluded; matching stays within a text node. No stored HTML rewrite or full matching on student GET.

Publication and alias changes queue scans. Admin processes bounded work; regenerate_connections drains oldest pending work fairly. Reads recheck revision/hash, proposal/alias approval, target and ancestor publication; withdrawals suppress links on the next request. SafeHtml sanitizes first, then inserts trusted local controls only from exact validated spans; authored attributes cannot forge them. Popup context revalidates on activation, uses escaped text and a safe new-tab route. Focus trapping/restoration, Escape/close/outside dismissal and mobile positioning remain.

Related topics combine approved relationships and current published syllabus associations, uniquely capped at six. Rejecting one phrase does not revoke an independently published syllabus relationship. Approved tag pages use released M2Ms, stable slugs, pagination and live eligibility. No unreliable shared process cache exists. Indexed candidates/prefetches support distinct canonical practice; 50-question pages and keyed signed manifests bind grading to current reviews and preview membership. Current publication resolution is bounded at 5,000 entries; production-scale benchmarking remains pending.

DOMPurify SafeHtml is the browser educational-HTML insertion boundary; SafeMarkdown disables raw HTML for AI output. Server nh3 sanitization, current publication and reviewed-file boundaries are independent checks. Search uses bounded database topic-title/published-note/approved-PDF queries, whitespace/case normalization and difflib typo suggestions; drafts/private files are excluded.

## Tutor and database boundaries

Current retrieval is bounded lexical ranking of published notes/approved PDF pages and, with opt-in, up to two reviewed related topics. Selection validates source ID/revision/text. History is not factual evidence. Server-built citation manifests, response validation, quotas and spend reservations bound the existing adapter; live AI defaults off. Strict current-topic-only retrieval and topic-note PDF export remain pending master Phase C, not completed features. See AI_SYSTEM for limits and billing caveats.

PostgreSQL is mandatory for normal/production runtime, with no implicit original-SQLite fallback. Original SQLite remains content 0004; schema source includes unchanged migrations 0001–0008. Explicit test/demo configurations are isolated. Prior migration/transfer/sequence/native-restore rehearsals used disposable copies; they do not authorize real cutover or prove durable production recovery.

## UI requirements consolidated from the retired design document

Use the existing components, routes and tokens; targeted maintenance must not introduce a new search, admin SPA or wholesale redesign. Source of truth is src/styles/tokens.css, src/App.css and src/styles/study.css.

| Token family | Light | Dark |
|---|---|---|
| Canvas / surfaces | #f8fafc / #ffffff / #f1f5f9 | #0b0f17 / #111827 / #1e293b |
| Text / muted | #0f172a / #475569 | #f8fafc / #cbd5e1 |
| Primary / hover | #1e40af / #1e3a8a | #60a5fa / #93c5fd |
| Lines | #e2e8f0 | #1e293b |

Retain readable system/Inter typography, restrained shadows/radii and the sun/moon toggle with system preference and prepal-theme persistence. Motion tokens use 140ms/220ms and cubic-bezier(0.16,1,0.3,1); reduced-motion overrides reduce transitions. Automated contrast evidence is not AAA certification or manual assistive-technology proof.

- Header: logo left, empty center, existing /search entry and theme toggle right on desktop/mobile; no auth/Syllabus/About header links. Preserve routes and footer Syllabus/Search/Help navigation, academic branding, honest dynamic counts and noninteractive future social space.
- Homepage: retain the existing RajasthanMap SVG geometry/aspect ratio and compact responsive spacing. Keep Explore Syllabus, source-aware assistant copy and two honest statistics. Root buttons scroll/focus actual API subjects without filtering or changing routes; no duplicate hero/explorer search/status controls.
- AppShell shares one hierarchy response through SyllabusContext/useSyllabus. Derive counts from all returned roots/descendants, including genuine zero data and loading/error/retry states. Do not truncate fixtures/future data to five; five roots are the original syllabus, not a UI constant.
- indexSyllabus derives numbering from original unfiltered order: numeric roots, dotted immediate children and per-parent alphabetic deeper children (AA after Z). Preserve titles/slugs and filtered original positions. Expand All opens all nodes; Collapse All leaves root labels; individual native-details toggles work after either. No Default View control. Standalone syllabus filtering remains separate from homepage simplification.
- Reader: preserve approved links, popup context/focus/new-tab behavior, tags, related topics and stateless practice. Keep one nonmodal bottom-right Tutor launcher, passage entry, responsive close/Escape/focus restoration without scroll loss; remove no existing reading ability or activate learner state.
- At mobile/tablet/desktop widths, maintain readable layouts, wrapped subject buttons, visible focus/labels and no horizontal overflow. Existing browser coverage sampled 320/390/768/1024/1280px; this is viewport emulation, not physical-device or manual screen-reader certification.

## Development samples and release inputs

Versioned sample tooling uses the canonical 142-topic fixture, existing review/publication services and a NEW isolated destination; no automatic startup/GET seed. It refuses existing/populated/symlinked targets, marks non-production engineering approval and never transfers original records. The query-only verifier checks corpus/API/CSRF/practice while blocking provider/network construction. Existing sample/demo data is preserved.

Shared workspace exclusions hide installed dependencies/generated/private trees without deleting them. scripts/release_manifest.py defines explicit source/config/test/canonical-doc inputs and rejects missing/symlinked/ignored/private inputs or known local credentials. Canonical cleanup produces 211 worktree release files; a manifest export is not a committed release. Historical evidence/recovery remains private. See [verification](TESTING.md) and [release gates](DEPLOYMENT.md).
