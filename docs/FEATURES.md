## Hosted synthetic-login candidate, publication batch

Prepared: public homepage/auth entry, student-gated library/APIs, original-route login return, controlled synthetic account workflow, one-hour secure sessions and read-only boot checks for the existing Render service. The prior local UI/session/ownership functionality is included. Registration, password recovery delivery, Google, Gemini, uploads and Admin content writes remain disabled. Not activated: no live account insertion, privilege/configuration change or deployment in this batch. Public real-user enrollment remains blocked by durable-data and operational acceptance.

---

## Local-only student access preview

Implemented in a separate synthetic PostgreSQL profile: public homepage and auth pages; guarded learning routes and API access; original-route login return; persistent session/logout/expiry handling; owned bookmarks/completion/planner/saved practice using existing services; independently authorized read-only Admin. Sign Up displays a closed-registration explanation without input fields. Public registration, hosted student data, email recovery, uploads, Google and Gemini are not enabled. The deployed restricted free demo remains unchanged.

---

## Live restricted demonstration

25 October 2026: the existing restricted demo is LIVE at https://rspc-ras.onrender.com. Render deployment dep-dbevgpfavr4c73c9m9i0 succeeded for main commit d2f014c186acba1360e9438a2382d13b85e74c6a at 18:11 IST. Matching GitHub Actions40171764725 is green. Account kartikyasokhal28@gmail.com / My Workspace / Prepal / Staging; existing Free web srv-dbe6d5vb9u1s738ikh80 and existing PostgreSQL dpg-dbe7a1oae00c73c5g090-a only. No new resource, purchase, upgrade, production release or valuable-data cutover.

Exactly30 migrations applied (content0001–0012 plus18 framework migrations),142 original syllabus topics/five subjects,15 sample note lessons,15 quizzes,75 questions,300 choices,19 tags,15 aliases,30 publications including ancestors,30 curated relationships and30 approved links. Exactly one synthetic view-only staff sample-editor, zero students/uploads/bookmarks/progress/saved attempts/AI requests. Engineering sample notices and quiz review reasons are not human academic approval.

Actual hosted Chrome checks passed: homepage142/five counts,142-link full expansion/five-root collapse, light/dark toggle, all15 sample lessons and their approved links/tags/related content, popup focus/new-tab attributes/Escape/focus restoration, three tag pages with exact counts, Monsoon search, all five subject practice pools and75/75 correct stateless scores, synthetic Admin login/session persistence/view-only detail/logout and five loaded Admin stylesheets. Config reports demo=true and student/AI/Google=false. Learner API error codes verified for guests and logged-in staff; Tutor request rejected as unavailable before provider work. HTTPS health200/status ok; unauthenticated homepage/config/Admin401 with Basic challenge, private/no-store/noindex; HSTS/nosniff/frame DENY verified. Keyboard skip-to-main, one main/one h1, no unnamed buttons and no horizontal overflow passed at1512px. This is a desktop browser smoke check, not a fresh mobile/axe/screen-reader/load audit.

Learner/AI/Google/email/uploads and Admin content edits remain disabled; no real student collection or production approval. Existing generic AI/verified-note copy is a presentation limitation, not an enabled or academically approved capability. Owner explicitly waived permanent independent/off-device recovery-key custody ONLY for this disposable synthetic database; durable custody remains unconfirmed and production safeguards are not waived. A real read-only native pg_dump17.11 CMS AES256GCM snapshot now contains40tables/1237rows/zero uploads, encrypted to the dedicated owner certificate. Private snapshot/receipt are in ../.recovery/prepal-live-deploy-xjhhgl_i/hosted-encrypted-backup/. The dedicated key/restore tooling passed the earlier independent LOCAL PostgreSQL17 restore; this hosted snapshot was not restored live. No daily scheduler, off-host retention or production30-day guarantee is configured. Free cold starts/expiring DB remain unsuitable for valuable data.

---

# Feature inventory

Published runtime source is main/d2f014c. The feature matrix includes locally verified student functionality, which is deliberately disabled in the hosted free demo. Hosted synthetic acceptance is recorded above; production acceptance is separate.

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

Locally implemented Render same-origin SPA/Admin/API serving, restricted staging access, explicit secure configuration and non-migrating build/start commands. The restricted synthetic free demo and PostgreSQL17 verified TLS are now hosted/accepted as recorded above. Durable production media, off-host recovery and live external-service acceptance remain pending. Tutor conversation now supports keyboard focus for its scrollable region. Learner/AI/Google access remains closed in staging/production profiles.

Render-only synthetic student acceptance has a separate explicit two-flag/database-name/private-access guard; normal staging and production remain closed. Only the hosted free-demo acknowledgements are enabled; synthetic student-acceptance flags and normal production/student/AI gates remain closed.
