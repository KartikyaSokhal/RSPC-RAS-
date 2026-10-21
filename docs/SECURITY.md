# Resolved local Django-key exposure — 21 October 2026

Confirmed that ignored backend/.env's SECRET_KEY matched one historical backend/core/settings.py blob present in two reachable commits: e6e7989db8c24eee59f8c38600cd619939c96856 and 84186c913572ca3edde66572b8f2f2c8409ba6eb. Read-only SSH confirmed remote main still at the first commit. Treat the old value as disclosed regardless of repository visibility; unauthenticated GitHub API 404 cannot establish visibility. No secret value is printed here.

**Remediation:** normal development settings loaded that key before rotation. The environment is development (DEBUG true, production mode unset); no matching inherited shell key or running application server was found. A scoped rpsc workspace text scan found only backend/.env using it. Replaced that one field atomically using 64 random bytes, made the file 0600 and verified Django loads the new value. Other environment fields are byte-semantically unchanged. No old-key fallback, production secret access, history rewriting or database/media writes. Existing production validation rejects the retired insecure-prefix key. Scoped scans exclude dependency/cache/Git/archive trees and large/binary files; external machines/production reuse cannot be assessed. Backups retain the inactive value privately for recovery and must never be used to restore it as an active secret.

**Impact:** old database-session signatures/auth hashes, password-reset links, visitor cookies and signed practice manifests no longer verify. Reauthenticate/reload practice; visitor/quota HMAC identities change in development. Password hashes, user/content records, old session rows, quotas/attempt history and media remain stored. No CSRF-secret rotation, password reset or content rewrite was performed. Independent demo/test keys are unchanged. Nine disposable in-memory checks verify these boundaries without writing source databases.

**Broader scan:** official Gitleaks v8.30.1 Darwin arm64 binary was downloaded privately and matched its published SHA-256. Default rules, full redaction, recursive decoding and ignored allow-comments were used on staged diff, all 223 indexed files and all reachable history; all returned zero findings. Separate exact matching against current environment/demo credentials plus the retired value found no active credential exposure and only the known retired historical blob. Default scanner rules did not flag that insecure development key; exact checks are necessary. No scan proves absence of all unknown secrets. Tool reference: [Gitleaks usage](https://github.com/gitleaks/gitleaks#usage).

No additional unresolved high-risk finding was identified within the inspected local scope. Production credentials and external reuse remain outside verification. No push, live AI, real cutover or deployment. Phase B requires separate approval and remote CI verification. Prior security sections below describe their dated batches.

---

# Controlled-cleanup release protection

A private full-worktree recovery snapshot includes modified, untracked, ignored and Git files; every file/symlink was verified, and the original database was independently restored and checked. It remains outside cleanup/release targets. Retired source/environment archives retain verified contents. Original/demo databases, media, migrations, historical evidence and dormant learner code are protected by hash comparisons.

The screenshot script no longer embeds a password or personal path. It requires a private absolute demo root, validates loopback/demo configuration, loads credentials privately and writes only private screenshots; no learner report is captured. Do not publish private backups or rotate/edit existing demo credentials as an incidental cleanup step.

The release allowlist rejects missing/symlinked inputs, private artifact types, ignored required inputs and any known private environment/demo credential found in release bytes. This is a concrete local-value check, not an exhaustive secret-history or vulnerability audit. Canonical docs remain public-safe/trackable; private history/evidence/design/proposals are excluded. Build/test dependencies remain locked and are installed separately in a clean disposable release copy. No paid provider is called.

---

# Sample-content isolation — 21 October 2026

Preparation exclusively creates a new private directory and explicit marker. Existing destination paths, symlink aliases to existing directories and populated topic/user/tag databases are refused; there is no reset, merge or overwrite flag. The seed uses core.demo_settings and requires its exact SQLite destination, excluding normal PostgreSQL settings. It reads checked-in fixture data, never original learner/content records or private environment values. Record creation is transactional and uses existing review/publication/connections services.

The verifier enables SQLite query-only mode, blocks network/provider construction and verifies the actual API/CSRF boundary. Notes and review records explicitly mark demo-only approval. Real editorial approval is not inferred from test passing. Credentials stay in the private ignored demo directory. No seed creates learner records, invokes a model or enables learner endpoints. Existing source/config/migration hashes are checked after verification.

---

# Phase 3 current discovery security

The approved Phase 3 brief supersedes prior discovery exclusions only. Learner containment, private storage, default-off paid AI, source preservation and real-cutover gates remain.

Only current published topic titles and approved aliases may target reviewed inline proposals. Decisions bind exact published source HTML hashes/revisions; repeated identical analysis preserves them, changed source evidence needs new approval. New aliases/tags/content do not auto-approve links. Ambiguous phrases, self-links, raw drafts and withdrawn target/ancestor content fail closed. Public tag approval defaults false and tag URLs are stable.

Matching and link-plan selection run in editorial workflows only. Student responses read a bounded plan and recheck proposal approval, revision/hash, alias/title eligibility and current publication. No HTML rewrite occurs. SafeHtml sanitizes first, then creates local popup anchors from exact validated span metadata with DOM APIs; authored data attributes cannot forge those controls. Popup descriptions are escaped text from a freshly checked published context endpoint. Full-topic actions use a new tab with noopener/noreferrer. Existing HTML/Markdown allowlists are unchanged.

Syllabus practice prefetches canonical questions from current reviewed quiz containers. Signed/keyed manifests bind the preview, page and membership; grading revalidates eligibility and shares existing +1/0 deterministic rules. CSRF is required; no Quiz, Question copy, saved attempt or learner identity is written. Review changes, withdrawals and foreign choices fail closed.

Normal Admin permissions protect suggestion decisions and explicit tag publication. Direct SQL/bulk changes to snapshots/registry remain unsupported editorial workflows. Inactive browser tabs are not polled; context is revalidated on popup opening and all routes re-evaluate eligibility on requests. No public response triggers regeneration.


# Phase 2 editorial boundary

All Phase 1 learner, paid-AI, storage and cutover restrictions below remain. Saving notes never republishes, including standalone ContentBlock Admin. Only explicit reviewed publication changes the released snapshot/tag M2M. Tags/aliases are controlled editorial records; aliases start draft and have no public matching/rendering behavior. Only approved TopicRelation edges enter new snapshots; withdrawn/draft edges are suppressed centrally from existing resolved publications. New/moved MCQ associations must be leaf subtopics in Admin and cannot repeat the primary as related; reviews also reject that overlap.

Question classification changes invalidate quiz review/revision tokens. Lossless legacy primary backfills preserve prior fingerprints. Maintenance routes enforce permissions directly: ordinary editors cannot use ResourcePage or QuizReview maintenance even if those model permissions were mistakenly assigned. Editorial staff receive no new permissions automatically. Normal Django Admin session/CSRF and escaped validation/message behavior remain.

HTML sanitization is unchanged. Empty WYSIWYG placeholder normalization fixes incomplete extra inline rows; it does not relax allowed HTML. Registry validation covers Unicode expansion and partial-save normalization. Direct bulk SQL/ORM updates bypass model normalization and are unsupported editorial operations. No student login, public tag discovery, automatic links, paid request or real database migration was introduced.

# Phase 1 security boundaries

The approved release is content-first. PostgreSQL configuration is primary, with no implicit SQLite fallback. Real data cutover is separate from local rehearsal approval.

## Learner containment

`content/urls.py` routes every public authentication/profile, dashboard, bookmark, progress, saved-attempt and weakness path to a constant 503 `learner_features_unavailable` response. It performs no authentication/body parsing/ORM operation. Guest, student, staff and superuser identities cannot bypass it. Dormant implementations are not registered. Learner models, nullable ownership fields, constraints and historical rows are retained; no ownership is inferred.

Public responses never query or expose learner state, including owned records. React does not mount its learner AuthProvider or probe session status. Student links/forms are absent; direct login/signup/dashboard URLs explain unavailability; topic controls are disabled. Stateless quiz checking remains CSRF protected and does not create attempts.

Django Admin retains normal staff authentication and editorial permissions. Bookmark/progress/attempt models and history stay inaccessible. Student reports deny every identity. Superusers may manage staff accounts only; nonstaff users are filtered and direct URLs cannot retrieve them. A student API logout cannot flush the administrative session.

## Content and files

SafeHtml remains the browser HTML insertion boundary; AI uses raw-HTML-disabled Markdown. Server publication sanitization, source references, review fingerprints and current eligibility checks remain active. Upload/preparation is not approval: Admin PDF preparation leaves resources ready for explicit text/rights review and does not republish a topic automatically.

The former unconditional private-media URL route was removed. Legacy ContentBlock attachment records remain stored; public responses withhold raw attachment links. Move approved PDFs through the existing LearningResource review workflow. Validated image and approved PDF routes remain functional. File storage stays local/private; PostgreSQL migration does not move media into database blobs.

## Database and recovery

Production configuration requires explicit PostgreSQL settings, strong Django startup configuration and verified TLS (`POSTGRES_SSLMODE=verify-full`). No production SQLite setting is accepted. Test/demo SQLite is selected explicitly and never automatically opens the original database.

Rehearsal creates a new loopback `prepal_rehearsal_*` target and checks it contains only fresh migration metadata before transfer. It reads a migrated copy in SQLite read-only mode. Framework and migration IDs, through-table rows, timestamp/JSON fields and historical sequence high-water marks are verified. Source/target migrations must genuinely have executed the same graph; no fake migrations are used. PostgreSQL test runner refuses existing test databases and nonlocal/nondisposable names.

Budget reservations use conditional global-row updates on both engines. Settlement locks AiRequest on PostgreSQL before checking its state, preventing double release of the same reserved cost. Concurrency verification uses synthetic requests and no AI provider.

Never print real environment values, credentials or private rows. Generated credentials, dumps, source copies and worktree archives remain private, outside Git. PostgreSQL native backups require an independent verified restore and a coherent private-media backup. Local temporary artifacts do not establish durable disaster recovery.

## Remaining gates

Owner review and explicit approval are required for actual cutover/credentials/deployment. AI defaults off; approved model/rates/cap and live factual evaluation remain pending. Remote CI, target-host TLS/proxy/parser/load behavior, durable backup retention and real content/rights review are not established by local tests. See [procedure](DEPLOYMENT.md) and actual evidence (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).
