# Security boundaries and release hold

Current authority permits only approved documentation/ignore cleanup and local checks. No credential rotation, migration, production change, commit, push, merge, deployment or history rewrite. [Handoff](AGENT_HANDOFF.md) records the current branch/commit and next approval gate.

## Confirmed exposure and retired credentials

The last read-only GitHub audit found the retired Django development key in remote main's backend/core/settings.py at line 27. One blob remains reachable through these historical revisions:

- `e6e7989db8c24eee59f8c38600cd619939c96856`
- `84186c913572ca3edde66572b8f2f2c8409ba6eb`

Remote development/PR merge heads and local release 49407b2 omit the literal but retain its ancestry. Do not deploy the old main tree as-is. Updating a branch head through a future approved normal release will not purge old history, forks or cached copies; history remediation requires separate explicit approval.

Prior authorized local remediation confirmed development-only use, replaced only ignored backend/.env's value using 64 random bytes, set mode 0600 and retained no fallback. Nine isolated checks verified old session/reset/cookie/practice signatures fail, new signatures work and passwords remain unchanged. Development visitor/quota HMAC identities change; existing rows/data/media were retained. Independent synthetic demo/test keys remain distinct. This cleanup must preserve the rotated file byte-for-byte, never restore a retired value from private backup, and never print credentials. Current production validation rejects insecure-prefix keys, but external reuse remains unverified; rotate any affected external environment only under separate approval and generate independent production secrets.

The audit found no real .env or credential/database/media/backup/generated file tracked in inspected local/remote history. Only the two .env.example templates occurred; their sensitive fields are blank. Active local environment/demo credentials had no exact match in Git objects. Standard author-email metadata is present in Git; no non-fixture personal contact/home-path content was found by scoped checks. Repository visibility, unadvertised/deleted refs, forks, cached artifacts and external systems were not established.

Gitleaks v8.30.1 default rules missed the known insecure-prefix development key; independent exact-value checks remain required alongside redacted scanner runs. No scanner guarantees detection of every unknown credential. Keep reports/dumps/mirrors and private recovery outside release inputs.

## Public content, files and learner isolation

Every public learner/auth/profile/dashboard/bookmark/progress/attempt/report path fails closed for all identities without exposing stored learner state. Dormant models/handlers/data are not feature authorization. Admin staff authentication remains; superusers alone manage staff accounts. Stateless grading requires CSRF and stable signed preview/review membership, never saved attempts.

Explicit reviewed publication controls all public notes/search/resources/context/tags/related/practice/Tutor sources. Draft/withdrawn/ancestor eligibility is rechecked; no draft fallback. Saving notes or extracting PDFs never auto-approves/publishes. Legacy raw attachment/private-media URLs remain withheld, while reviewed resource/image routes retain hash/eligibility checks. Uploads/extraction are bounded and require rights/text review; no arbitrary remote fetch or new OCR.

Server nh3, browser educational DOMPurify SafeHtml and raw-HTML-disabled SafeMarkdown remain independent boundaries. Approved phrase controls are inserted only after source/span validation; student GET never performs expensive suggestion matching or writes HTML. Alias/tag/proposal/relationship review and current target publication are mandatory. Editor bulk SQL that bypasses validation is unsupported. Popups revalidate on opening; no cross-origin executable content.

## Tutor, database and operational controls

Existing AI uses bounded current/opt-in-related published evidence, server citation manifests, selection/revision checks, conservative spend reservations, quotas, timeouts and one provider attempt. Live defaults off; model/rates/cap/budget and quality need explicit review. Strict current-topic-only retrieval remains Phase C work. See [AI_SYSTEM](AI_SYSTEM.md); no paid requests are authorized here.

Normal production configuration requires PostgreSQL, strong independently generated secrets, explicit hosts/CSRF origins and verify-full TLS. No original-SQLite fallback is permitted. Least-privilege roles, trusted proxy overwrite rules, private media and durable encrypted DB-plus-media restore/retention need approved target-host validation. Prior disposable transfer/sequence/restore tests are not real cutover or durable recovery.

Real .env/credentials/databases/media/backups/environments/output/history remain ignored/untracked. Approved extra ignore patterns cover private keys/containers/dumps/tokens and credentials without hiding safe templates, SQL source or public CA certificates. The release manifest rejects private/ignored/missing/symlinked inputs and known local credentials; it is not a complete secret scanner. Never print private records/prompts/passwords or reactivate ownerless learner data.

## Remaining risks

Review retired-key exposure still visible on audited GitHub main/history and any external reuse before publication. Also pending: human content/rights review, real PostgreSQL roles/TLS/cutover/durable recovery, domain/static/media/proxy/Admin/load/monitoring validation, live AI evaluation/budget, PDF timeout alignment and unimplemented topic-note PDF export. Production/staging access or deployment is not established. Actual current versus historical checks: [TESTING](TESTING.md).
