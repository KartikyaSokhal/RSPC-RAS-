## Hosted public-homepage synthetic-demo candidate

A new core.render_public_demo_settings composes production-strength settings, same-origin SPA/API/Admin/WhiteNoise delivery and the shared student-session middleware without StagingAccessMiddleware. It accepts only the existing external Render host/database/runtime role and exact HTTPS origin, preserves verify-full and uses one-hour HttpOnly/Secure/Lax host-only sessions. Only the privately designated synthetic identity is eligible; arbitrary StudentIdentity users and staff sessions are denied learning APIs. Signup/reset/Google/AI/uploads/Admin mutations remain closed. Original production, staging, free-demo and local-only profiles are unchanged.

The existing operator CLI gains private-password preparation and a guarded student-login transition on the initialized corpus. The migration owner verifies the original known state, creates one synthetic User/StudentIdentity, extends the existing initialization marker and grants fixed owned-record/row-lock privileges atomically. Unknown data/accounts are preserved and refused; repeated use verifies the same password without reset. The default original initializer remains zero-student and refuses the extended state. Public-state verification explicitly validates the marked user and owned rows while retaining exact canonical corpus/review checks. Boot uses shared strict schema checks, batched counts/privileges and migration/account/marker checks; exhaustive corpus revalidation belongs to operator preflight. No new schema or migrations.

---

## Local student-gated preview — current addition

`core.public_demo_settings` extends the guarded local PostgreSQL candidate, verifies a ready synthetic marker bound to the database name, and adds StudentLearningAccessMiddleware after Django authentication. The exact public API allowlist is health/config/session login/logout/status/closed register. All other API paths fail closed for guests, inactive, staff or unbound Django users; session authentication never emits a Basic challenge. Admin retains Django staff authorization and synthetic read-only restrictions. No models, migrations or existing deployment profiles changed.

React LearningRoute wraps syllabus/topic/quiz/practice/tags/search/resources/dashboard/planner/attempt routes only when config.learning_auth_required is true. AppShell defers hierarchy requests until session verification succeeds and uses intentionally public aggregate counts for guests. Login preserves a validated local pathname/query/hash, including across the Sign Up link. AuthProvider refreshes on focus/pageshow, invalidates on auth_required responses and discards stale status replies after login/logout. Account changes still remount page state. SafeHtml, Phase 3 discovery and existing content-first routes retain their original behavior outside this new profile.

---

## Explicit free-demo database operations

scripts/free_demo_database.py selects only protected operator files and delegates schema/corpus initialization to initialize_free_demo; ordinary build/start remain non-migrating. The dedicated operator settings require exact remote identity/TLS/free-demo acknowledgements or an explicit bounded loopback test target; no SQLite fallback. A separate minimal migration role owns app objects; runtime reads content and writes only session/auth bookkeeping. Canonical sample_install is shared after each caller's original safety guards; production publication/retrieval behavior is unchanged. PostgreSQL advisory locking, atomic DDL/data/marker and strict verify-only repeats prevent resets/adoption of unknown data. One operator-owned completion table is outside Django models/migrations.

---

## Restricted Render Free demonstration

core.free_demo_settings is an explicit alternative, separate from existing production/staging profiles. It imports normal strong production settings, then requires free-demo identity/two synthetic acknowledgements, full external-host TLS with a trusted CA, exact HTTPS origin and the existing independent staging password barrier. It reuses reviewed Render SPA routes/static serving; free_demo_urls adds a minimal database-readiness503 boundary. No source schema or production policy changed.

FreeDemoRestrictions rejects multipart before parsing and Admin content-changing requests (synthetic staff login/logout remain). DisabledUploadStorage denies uploads, file reads/deletion and media URLs; no persistent or valuable ephemeral file storage exists. Student/AI/Google flags and provider keys are disabled in runtime regardless of opt-in environment values, without altering stored environment secrets. Read-only content/search/reviewed stateless practice remain; only an explicitly synthetic disposable PostgreSQL target may be selected. Test browser adapter substitutes a newly prepared SQLite fixture only in private test settings, not in deployable profile.

---

# Architecture

Prepal is a React 19/Vite SPA plus Django 6/DRF, Django Admin and PostgreSQL. The student platform extends existing models/routes/components; no duplicate application stack is introduced. [Database schema](DATABASE_SCHEMA.md), [API](API_DOCUMENTATION.md), [Admin workflow](ADMIN_WORKFLOW.md) and [AI system](AI_SYSTEM.md) describe their detailed boundaries.

## Runtime and identity

Vite proxies same-origin /api to private Django during local development. Reviewed Nginx/systemd/Gunicorn examples live under deploy/ and backend/gunicorn.conf.py; they are not an installed/verified production service. Static output and private media are separate. No retired Express/Mongo launch path remains active.

Django sessions now serve owned student accounts as well as administrative identity, with CSRF, HTTP-only cookies, 14-day expiry and production secure cookies. StudentIdentity binds normalized unique email and optional unique Google subject to the existing User. AuthRateWindow uses HMAC keys. Google state/nonce/PKCE and signed issuer/audience/expiry/email checks prevent client identity claims and automatic account linking. Password reset tokens are single-use and not stored. No auth token is stored in localStorage.

STUDENT_FEATURES_ENABLED defaults false in production; a closed gate returns constant unavailable responses before authentication/body parsing. Enabled handlers query request.user exclusively and never adopt ownerless rows. Dashboard, subject progress and planner share published content-bearing unit eligibility. Explicit POST visits update history; GET does not. StudyPlan/StudyTask use deterministic estimates/calendar allocation, revision conflict checks and completed-row preservation. Canonical practice remains stateless for guests; enabled students can save a UUID-idempotent immutable QuizAttempt snapshot. Existing Question records are not copied. Account changes remount private page state and refresh syllabus status.

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

Tutor retrieval is bounded lexical ranking of current published **note blocks only**. It excludes PDFs/related topics and refuses cross-scope requests. Selection validates source ID/revision/text; history is not evidence. Server manifests, repeated scope/publication checks, safe Markdown, quotas and conservative spend reservation constrain the existing adapter. Live Gemini defaults off and is not live-verified. Topic-note PDF export remains deferred. See AI_SYSTEM for precise limits.

PostgreSQL is mandatory for normal/production runtime without original-SQLite fallback. Migrations 0001–0008 are unchanged; new 0009–0012 cover identity, visits, planner and immutable practice. Original SQLite remains 0004 and existing demos remain unchanged. New review/demo/test targets alone receive the new migrations. Disposable PostgreSQL tests and source-copy/transfer/restore rehearsals do not authorize real cutover or establish durable production recovery.

## UI requirements consolidated from the retired design document

Use the existing components, routes and tokens; targeted maintenance must not introduce a new search, admin SPA or wholesale redesign. Source of truth is src/styles/tokens.css, src/App.css and src/styles/study.css.

| Token family | Light | Dark |
|---|---|---|
| Canvas / surfaces | #f8fafc / #ffffff / #f1f5f9 | #0b0f17 / #111827 / #1e293b |
| Text / muted | #0f172a / #475569 | #f8fafc / #cbd5e1 |
| Primary / hover | #1e40af / #1e3a8a | #60a5fa / #93c5fd |
| Lines | #e2e8f0 | #1e293b |

Retain readable system/Inter typography, restrained shadows/radii and the sun/moon toggle with system preference and prepal-theme persistence. Motion tokens use 140ms/220ms and cubic-bezier(0.16,1,0.3,1); reduced-motion overrides reduce transitions. Automated contrast evidence is not AAA certification or manual assistive-technology proof.

- Header: logo left, empty center, existing /search entry and theme toggle right on desktop/mobile; student Sign In/Sign Up when enabled and logged out; Dashboard/account/logout when signed in. Syllabus/About remain absent from the header. Preserve routes and footer Syllabus/Search/Help navigation, academic branding, honest dynamic counts and noninteractive future social space.
- Homepage: retain the existing RajasthanMap SVG geometry/aspect ratio and compact responsive spacing. Keep Explore Syllabus, source-aware assistant copy and two honest statistics. Root buttons scroll/focus actual API subjects without filtering or changing routes; no duplicate hero/explorer search/status controls.
- AppShell shares one hierarchy response through SyllabusContext/useSyllabus. Derive counts from all returned roots/descendants, including genuine zero data and loading/error/retry states. Do not truncate fixtures/future data to five; five roots are the original syllabus, not a UI constant.
- indexSyllabus derives numbering from original unfiltered order: numeric roots, dotted immediate children and per-parent alphabetic deeper children (AA after Z). Preserve titles/slugs and filtered original positions. Expand All opens all nodes; Collapse All leaves root labels; individual native-details toggles work after either. No Default View control. Standalone syllabus filtering remains separate from homepage simplification.
- Reader: preserve approved links, popup context/focus/new-tab behavior, tags, related topics and stateless practice. Keep one nonmodal bottom-right Tutor launcher, passage entry, responsive close/Escape/focus restoration without scroll loss. Learner buttons require the server gate, authentication and owned endpoints.
- At mobile/tablet/desktop widths, maintain readable layouts, wrapped subject buttons, visible focus/labels and no horizontal overflow. Existing browser coverage sampled 320/390/768/1024/1280px; this is viewport emulation, not physical-device or manual screen-reader certification.

## Development samples and release inputs

Versioned sample tooling uses the canonical 142-topic fixture, existing review/publication services and a NEW isolated destination; no automatic startup/GET seed. It refuses existing/populated/symlinked targets, marks non-production engineering approval and never transfers original records. The query-only verifier checks corpus/API/CSRF/practice while blocking provider/network construction. Existing sample/demo data is preserved.

Shared workspace exclusions hide installed dependencies/generated/private trees without deleting them. scripts/release_manifest.py defines explicit source/config/test/canonical-doc inputs and rejects missing/symlinked/ignored/private inputs or known local credentials. The manifest includes student source, migrations, corpus and browser tests; a worktree export is not a committed release. Historical evidence/recovery remains private. See [verification](TESTING.md) and [release gates](DEPLOYMENT.md).

The new student review corpus adds 25 drafts/125 MCQs at real previously unused lesson IDs. Existing sample publications remain synthetic; new material/aliases/relations/quizzes receive no automatic human approval. Private review inventory and original sources accompany the seed.

## Local student environment selection

The student UI reuses AppShell/AuthProvider and existing routes. Header order is Search, theme, guest Sign In/Sign Up or authenticated Dashboard/named Account menu/Logout. Normal settings now default learner access off in both development and production. Explicit ready student_demo_settings enables the owned flow. run_student_dev.py validates marker/schema0012 read-only and binds the student API on8002, separate from the content-only8000 service. Vite reads ignored .env.local PREPAL_DEV_API_ORIGIN in development only; server config/ownership/CSRF remain authoritative and build/preview routes are unchanged. No migrations/auth duplication or separate Profile page.

## PostgreSQL operations boundary

core.database builds explicit PostgreSQL config with bounded connect/statement/lock/idle-transaction timeouts and connection age. core.local_postgres_settings requires explicit local opt-in, loopback and prepal_local_/prepal_rehearsal_ name; no AI/Google. core.staging_settings and core.production_settings require separate matching environment identities and force learner/AI/Google closed. Active student-review SQLite is unchanged; configuration files alone are not a cutover.

content.services.postgres_ops provisions NEW local databases and separate restricted migration/runtime/backup roles; postgres_backup exports a read-only repeatable-read snapshot, native custom pg_dump and stable paired media inventory, then encrypts with OpenSSL CMS AES-256-GCM. Restore decrypts/authenticates first, rejects unsafe tar members, provisions a NEW local DB, pg_restores without owner/ACL replay and verifies all table hashes/IDs/FKs/sequence minima/media. It never restores roles or overwrites a target. Operators must select trusted archives: encryption authenticates ciphertext, not its sender or arbitrary SQL inside an archive. No production backup execution/off-host integration is enabled.

scripts/postgres_ops.py is a private-env CLI; scripts/rehearse_student_postgres.py composes copied-source migration/transfer, real HTTP backend restart/session checks, ownership, native encrypted restore and corruption tests. Tests use synthetic content only. Account/deletion is a non-destructive backend readiness boundary, not a new authentication system or deletion implementation.

## Prepared single-origin Render staging

The Render-only settings/URL modules add an explicit SPA route map, WhiteNoise serving of dist/collected staticfiles and a private HTTP Basic staging barrier. Existing development URLs and student session authentication are unchanged. Basic staging credentials never become DRF user credentials. API/private path404s remain real404s. Built SPA/API/Admin share HTTPS and host-only secure SameSite=Lax cookies; CORS stays empty. A paid media disk and verified PostgreSQL external TLS are prerequisites, not provisioned resources. See [deployment](DEPLOYMENT.md).
