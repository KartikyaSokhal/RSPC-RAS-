## Free-demo publication security review — 24 October2026

GitHub visibility is now Public, unlike the previous private-release observation. Owner explicitly approved publishing this reviewed candidate after disclosure of the changed scope and known retired Django key in reachable history. Retired key stays retired; no history/visibility rewrite. Required release/staged scans exclude real environment files, credentials, databases, media, backups and generated artifacts. Existing production/staging/TLS modules and private file hashes are preserved.

Render auto-deploy is Off before main publication. No secret/environment edits or redeploy; free-demo acknowledgements cannot be asserted until the live target is audited as synthetic. Internal host plus verify-full remains an explicit blocker, never a reason to lower TLS. Authenticated SQL/schema/roles and current hosted service security remain unverified.

---

## Restricted free-demo controls

Production/staging/shared database security files are unchanged. New profile requires explicit synthetic/free-demo opt-in, strong production secret/HTTPS/host validation, existing private access barrier and external PostgreSQL verify-full plus trusted CA. It rejects internal host and lower TLS modes. Actual external TLS1.3/certificate/hostname negotiation passed; no login or SQL was performed. Credentials were not exposed or changed; browser-redacted placeholders are not usable credentials. Do not invent a successful authenticated connection.

Students, signup/login, progress/planner/attempt saving, Gemini/Google/email are forced off. All multipart requests are rejected before parsing; default storage rejects writes/reads/deletion and Admin content-changing methods are blocked. Existing private media environment value is preserved but unused. Only synthetic staff sessions/content are allowed in the designated disposable DB, after read-only audit. Current live inbound rules include0.0.0.0/0 and were not changed: separately review/narrow before hosted acceptance. No production user data on free, expiring PostgreSQL; no valuable uploads to ephemeral web storage. Normal30-day encrypted production recovery requirements remain unfulfilled by free demo and unchanged.

---

## Staging publication security gate

Only the reviewed candidate may be committed/pushed, after verifying the complete Git index excludes real environment files, credentials, databases, media, backups and generated artifacts. Safe blank.env.example templates remain included. Scan the exact staged snapshot and compare known local/private and retired historical keys without logging values. The known retired Django key remains in historical commits and must never be reused; scanner silence does not erase that known exposure. No history rewrite. Render installation access is not granted by this batch; DEPLOYMENT provides the repository-specific least-privilege approval steps.

---

# Security boundaries

Current authority permits safe local student-platform implementation and disposable verification only. No commit/push/deploy, real cutover, production credential changes or paid provider requests. Production student access defaults off. See [handoff](AGENT_HANDOFF.md).

## Confirmed exposure and retired credentials

The last read-only GitHub audit found the retired Django development key in remote main's backend/core/settings.py at line 27. One blob remains reachable through these historical revisions:

- `e6e7989db8c24eee59f8c38600cd619939c96856`
- `84186c913572ca3edde66572b8f2f2c8409ba6eb`

Remote development/PR merge heads and local release 49407b2 omit the literal but retain its ancestry. Do not deploy the old main tree as-is. Updating a branch head through a future approved normal release will not purge old history, forks or cached copies; history remediation requires separate explicit approval.

Prior authorized local remediation confirmed development-only use, replaced only ignored backend/.env's value using 64 random bytes, set mode 0600 and retained no fallback. Nine isolated checks verified old session/reset/cookie/practice signatures fail, new signatures work and passwords remain unchanged. Development visitor/quota HMAC identities change; existing rows/data/media were retained. Independent synthetic demo/test keys remain distinct. This implementation preserves the rotated file byte-for-byte, never restore a retired value from private backup, and never print credentials. Current production validation rejects insecure-prefix keys, but external reuse remains unverified; rotate any affected external environment only under separate approval and generate independent production secrets.

The audit found no real .env or credential/database/media/backup/generated file tracked in inspected local/remote history. Only the two .env.example templates occurred; their sensitive fields are blank. Active local environment/demo credentials had no exact match in Git objects. Standard author-email metadata is present in Git; no non-fixture personal contact/home-path content was found by scoped checks. Repository visibility, unadvertised/deleted refs, forks, cached artifacts and external systems were not established.

Gitleaks v8.30.1 default rules missed the known insecure-prefix development key; independent exact-value checks remain required alongside redacted scanner runs. No scanner guarantees detection of every unknown credential. Keep reports/dumps/mirrors and private recovery outside release inputs.

## Public content, files and learner isolation

A closed STUDENT_FEATURES_ENABLED gate returns a constant unavailable result for all learner/auth handlers before parsing/authentication. When enabled, every learner route requires session ownership; mutations require CSRF. Other users' plan/attempt IDs return 404, ownerless legacy rows stay unassigned, and public serializers cannot expose global state. Only explicit owned POST visits write reading history. Logout/account changes discard private page state. Admin staff authentication remains separate; learner Admin reports stay closed.

Passwords use Django hashing/validation. StudentIdentity enforces normalized unique email and optional stable unique Google subject. Registration checks existing legacy User collisions. Google callback validates server-session one-use state/expiry, PKCE, signed token audience/issuer/expiry/verified email and nonce; no implicit email-based linking or persisted access/ID tokens. Production cookies are secure/HTTP-only/SameSite Lax; sessions expire after 14 days. Reset tokens expire after 30 minutes, become invalid after password change and travel in a cleared URL fragment rather than query/access logs. Request responses are generic, including SMTP delivery failures; configuration errors are identical for known/unknown emails. Password accounts do not yet verify email ownership. Set production verification/abuse policy and validate real SMTP/Google before enabling public registration.

DB-backed HMAC rate windows limit auth identities/IPs without storing raw identifiers. Visits, plan creation and attempt submissions have bounded rates. Window rows currently require an operational retention/pruning policy; no scheduled purge is enabled. Stateless checks keep existing signed-preview/CSRF validation. Saved attempts are immutable per-user snapshots with unique UUID idempotence and canonical-source locking/revalidation. History intentionally retains previously reviewed answers after content edits/withdrawal; it is accessible only to its owner.

Explicit reviewed publication controls all public notes/search/resources/context/tags/related/practice/Tutor sources. Draft/withdrawn/ancestor eligibility is rechecked; no draft fallback. Saving notes or extracting PDFs never auto-approves/publishes. Legacy raw attachment/private-media URLs remain withheld, while reviewed resource/image routes retain hash/eligibility checks. Uploads/extraction are bounded and require rights/text review; no arbitrary remote fetch or new OCR.

Server nh3, browser educational DOMPurify SafeHtml and raw-HTML-disabled SafeMarkdown remain independent boundaries. Approved phrase controls are inserted only after source/span validation; student GET never performs expensive suggestion matching or writes HTML. Alias/tag/proposal/relationship review and current target publication are mandatory. Editor bulk SQL that bypasses validation is unsupported. Popups revalidate on opening; no cross-origin executable content.

## Tutor, database and operational controls

Tutor uses current published note blocks only: no related/PDF/website/external evidence. Both retrieval and response citation scope are checked; obvious instruction overrides refuse before provider/spend. Safe Markdown, selection/revision checks, conservative spend reservations, quotas, timeouts and one provider attempt remain. These controls do not prove factual entailment or immunity to every prompt injection. Live defaults off; model/rates/cap/budget and quality need explicit review. See [AI_SYSTEM](AI_SYSTEM.md); no paid requests occurred.

Normal production configuration requires PostgreSQL, strong independently generated secrets, explicit hosts/CSRF origins and verify-full TLS. No original-SQLite fallback is permitted. Least-privilege roles, trusted proxy overwrite rules, private media and durable encrypted DB-plus-media restore/retention need approved target-host validation. Prior disposable transfer/sequence/restore tests are not real cutover or durable recovery.

Real .env/credentials/databases/media/backups/environments/output/history remain ignored/untracked. Approved extra ignore patterns cover private keys/containers/dumps/tokens and credentials without hiding safe templates, SQL source or public CA certificates. The release manifest rejects private/ignored/missing/symlinked inputs and known local credentials; it is not a complete secret scanner. Never print private records/prompts/passwords or reactivate ownerless learner data.

## Remaining risks

Review retired-key exposure still visible on audited GitHub main/history and any external reuse before publication. Also pending: human content/rights review, real PostgreSQL roles/TLS/cutover/durable recovery, domain/static/media/proxy/Admin/load/monitoring validation, live AI evaluation/budget, PDF timeout alignment and unimplemented topic-note PDF export. Production/staging access or deployment is not established. Actual current versus historical checks: [TESTING](TESTING.md).

## Explicit local student gate

Normal development now defaults closed as production already does. Only the explicitly selected ready student-review environment enables the local owned handlers; frontend controls follow /api/config/. The development-only proxy override does not change API gates, cookies, CSRF, ownership or Google readiness. Launcher --check uses query-only SQLite, refuses missing/incomplete/symlinked/legacy destinations, and never applies migrations. Original archives/media/credentials and old demos remain protected.

## PostgreSQL preparation and deletion approval gate — current

Safe local implementation is complete; production remains disabled. New local roles have unique generated passwords, SCRAM host authentication in the test cluster, no superuser/CREATEDB/CREATEROLE/replication/BYPASSRLS or role memberships. Runtime has ten connections and table CRUD/sequence USAGE/SELECT only; migration owner has two; backup SELECT/two. Runtime CREATE/ALTER/setval and backup DELETE/CREATE were denied; incorrect passwords rejected for all three roles. Separate0600 env files are stored outside the checkout. Retired key rotation remains intact; new candidate signing keys are independent. No production secret was accessed or rotated.

Production config refuses SQLite, missing password or TLS weaker than verify-full. Configure hostname-matching CA using POSTGRES_SSLROOTCERT; local tests verify refusal/config only because the private16.2 build lacks SSL. Neither production TLS connectivity, certificate rotation, public registration nor host monitoring is accepted. Django password validation/PBKDF2, CSRF/session ownership/14-day expiry, secure production cookies and30-minute one-use resets remain. New regressions verify another persisted session becomes unauthenticated after password reset. Registration409 still exposes identifier availability; email verification, registration-enumeration/abuse policy and SMTP timing hardening need production acceptance. Google remains off; no real external request occurred.

**Proposed retention rules — owner approval required, NOT implemented:** after authenticated current-password recheck and explicit permanent-loss confirmation, atomically erase the student's identity/User, bookmarks, progress/visits, plans/tasks and practice history, while preserving shared syllabus/content/canonical MCQs. Staff/editor accounts with publication/audit references require a separate controlled administrative workflow; do not cascade shared content or silently anonymize reviewer evidence. Revoke all user sessions; define support/audit handling and a non-PII deletion ledger to reapply accepted deletions after restore. Google-only users require an approved equivalent fresh verification flow; do not bypass reauthentication.

Proposed recovery retention: seven days for disposable local encrypted drills;30days for daily production encrypted DB/media backups, with approved deletion-ledger retention at least through the longest backup lifetime. Deleted account records can remain encrypted in backups until expiry and must be removed again before any restored system serves users. Confirm legal/support obligations, ledger design and restore operations before implementation. No automatic pruning, account erasure, anonymization or retention timer is enabled.

GET /api/account/deletion/ requires the student gate+authentication and returns only the caller's owned counts, deletion_enabled=false and policy_approval_required. POST rejects unknown/user_id fields, requires CSRF/current password/DELETE MY ACCOUNT, rate-limits attempts, and ALWAYS returns409 deletion_policy_pending after valid confirmation. It never schedules or performs deletion; DELETE405, guest401, closed gate503 before queries. This permits security verification without implementing irreversible behavior.

Backups use native pg_dump and CMS AES-256-GCM, private output permissions and a separately held recipient private key. Wrong key/tamper/truncation/non-AEAD CBC/path traversal are rejected. Only trusted locally selected dumps can be restored. Key custody/loss is an operational risk: losing the private key loses recovery access; copy it securely offline and do not co-locate it with production archives. Local source recovery snapshots are private access-controlled copies; the new PG workflow produces encrypted archives. Daily logical dumps alone offer at best24-hour nominal RPO, not PITR. Off-host immutable storage, monitoring, backup encryption/key rotation and retention are production gates; local successful restores do not establish them.

## Current Render staging controls and unresolved gates

The candidate retains verify-full, closed production/student/AI/Google settings and secure host-only SameSite=Lax cookies. Independent HTTP Basic staging access protects all frontend/Admin/API/assets except read-only health; credentials are stripped before DRF and never establish a student session. New credentials must be private and distinct from the retired Django key. No credential was transmitted to Render/Vercel. Render GitHub access expansion needs owner approval for this repository only.

Render internal PostgreSQL self-signed TLS cannot meet verify-full; test external hostname/CA with restrictive outbound-IP allowlisting before migration/data. Proxy client-IP overwrite, application/Admin rate limiting, host resource limits and hosted TLS/storage remain unverified. Learner access stays off. Owner approved30-day daily encrypted production backup retention, but off-host storage/key custody, scheduler/alert delivery and hosted restore are outstanding. Do not enable deletion/pruning or claim Render3-day Hobby PITR meets30days.

Render-only synthetic student acceptance has a separate explicit two-flag/database-name/private-access guard; normal staging and production remain closed. No hosted flags were enabled.

Staging security audit initially found PYSEC-2026-4320 in certifi2026.10.18 and CVE-2026-114136/114137/114138 in DRF3.17.2. Updated to the upstream fixed certifi2026.10.19/DRF3.18.2 and regenerated both hash locks; final runtime advisory scan is clean. This required clearing Django's cached Authorization mapping after staging Basic authentication so patched DRF does not treat the separate staging credential as a student credential. No token-auth system was introduced.
