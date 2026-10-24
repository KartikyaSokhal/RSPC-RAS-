## Free Render demo candidate — local only

Prepared password-protected React/API/Admin/static demo with forced-off student accounts, progress/planner/attempt saving and AI/Google/email. Reader content/discovery and stateless reviewed practice reuse existing code. Admin content mutations and every upload are disabled; no valuable data/media is accepted. Strict external PostgreSQL TLS is retained; only TLS negotiation is verified live, not SQL/schema/content. No new deployment was made. Free database expires23November2026 and is not production storage.

---

# Feature inventory

Current implementation is uncommitted work over 8ef43c7 on codex/prepal-1-0. Verification is local, with isolated databases and mocked external providers; it is not production acceptance.

| Feature | Implemented behavior | Limits |
|---|---|---|
| Reading and discovery | Original syllabus/slugs/numbering, published notes, safe rich text, search, approved resources/images, links/popups, tags and related topics | Publication and ancestor eligibility required |
| Content management | Django Admin, draft/private preview/review/publish/withdraw, controlled metadata, canonical reviewed MCQs | Human academic/rights review remains mandatory |
| Accounts | Email/username password sessions, registration/logout/reset, Google authorization-code flow | Google credentials/consent and SMTP delivery unverified; password email verification deferred |
| Dashboard | Owned completion/bookmarks, weighted accuracy across all attempts, subject progress/performance, visits/continue/next lessons and plan targets | Empty structural topics excluded; no invented counts |
| Saved learning | Idempotent owned bookmark/completion, explicit visits; legacy ownerless records never adopted | Production gate defaults closed |
| Planner | Owned plans, published branch selection, approximate duration, weekdays/capacity, Learn/Revision modes, daily/weekly/monthly output, exam feasibility, edits/rescheduling | Default 90-minute estimate is editable; task completion is separate from whole-lesson completion |
| Practice | Reviewed stable signed quiz/collection preview, stateless guest grading, owned UUID-idempotent attempts and immutable answer snapshots | One canonical question; no AI generation or GET writes; legacy attempts lack detailed snapshots |
| Tutor | Current published note evidence only, selected passage, explain/summarize, source citations, refusals, quotas/cost reservation | Mock verified; live Gemini off and not live-validated; PDFs/related lessons excluded |
| New review corpus | 25 new real-syllabus lessons, 125 MCQs, 500 choices, source inventory and draft relationships | Isolated drafts, not public/human approved; existing 15-lesson sample preserved |

One eligibility rule is shared by dashboard, subject progress and planner: a currently visible publication with nonempty note text or an approved PDF attached to its released snapshot. Structural headings are excluded. Bookmarks may target any published topic. Overall quiz accuracy is total correct / total attempted questions, rather than an unweighted mean or a recent-history cap.

Preserved frontend behavior includes light/dark themes, original-order tree numbering, search, responsive footer counts, Phase 3 popups and one Tutor launcher. Account changes discard private page state and refresh owned syllabus flags.

Deferred: phone OTP, email verification policy, live Google/SMTP/Gemini acceptance, production DB cutover/hosting, human academic review/publication, topic-note PDF export and production load/manual assistive-technology testing. See [scope](MVP_SCOPE.md), [testing](TESTING.md) and [deployment](DEPLOYMENT.md).

## Local authentication navigation

Verified local navbar and existing signup/login/logout/session/dashboard routes are exposed only when the selected backend permits students. Authenticated users retain owned bookmarks/completion/planner. Guest/private isolation remains. The explicit student API is8002 and frontend5173; normal development/production gates default off. Google is disabled/unconfigured in this environment; SMTP/live OAuth acceptance remains pending.

## PostgreSQL preparation status

Verified locally: separate migration/runtime/read-only backup roles; bounded connection/timeouts; guarded local/staging/production profiles; fresh schema0001–0012 and ID-preserving student-source copy transfer; persisted accounts/password hashes/sessions/bookmarks/progress/visits/immutable attempts/plans/completed task history through restart and native restore; authenticated AES-GCM DB/media archives; corruption rejection and backup failure/age status. No model/migration changes in this task.

Readiness-only account/deletion endpoint protects authentication/CSRF/password/ownership and returns policy pending without erasing anything. Deferred pending owner acceptance: irreversible deletion/retention ledger, pruning, real PostgreSQL cutover, production TLS connectivity/PG17, off-host backup/alert delivery/scheduler activation, SMTP/Google/email verification and public learner release. Existing8002 remains isolated SQLite; all prior student/content/UI functionality is preserved.

## Staging preparation

Locally implemented Render same-origin SPA/Admin/API serving, restricted staging access, explicit secure configuration and non-migrating build/start commands. Hosted deployment, PostgreSQL17 TLS, durable media, off-host backups and live external-service acceptance are still pending. Tutor conversation now supports keyboard focus for its scrollable region. Learner/AI/Google access remains closed in staging/production profiles.

Render-only synthetic student acceptance has a separate explicit two-flag/database-name/private-access guard; normal staging and production remain closed. No hosted flags were enabled.
