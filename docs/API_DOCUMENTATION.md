# HTTP API

All paths below are under `/api/`. Normal operation is same-origin Django session authentication, HTTP-only cookies and CSRF-protected writes. Errors use `error.code` / `error.message`. Student/private responses are `Cache-Control: no-store`. Never accept a client user ID as ownership.

## Public reading and practice

| Method/path | Contract |
|---|---|
| GET health/, config/ | Health; public feature flags, Google availability, CSRF initialization; no secrets |
| GET topics/?tree=1, topic/:slug/ | Original syllabus/public snapshots; unpublished outlines expose no private blocks; owned flags only for enabled authenticated users |
| GET search/, tags/:slug/, topic/:slug/context/ | Publication-aware search/tags and revalidated approved popup context |
| GET resources/:id/, resources/:id/file/, topic/:slug/images/:block/ | Approved, released, hash/eligibility-checked resources/images |
| GET topic/:slug/quiz/ | One eligible reviewed quiz, stable ID and signed revision token; no generation/writes/provider call |
| POST topic/:slug/quiz/check/ | `{quiz_id, revision_token, answers}`; deterministic +1/0, strict membership/types; never saves an attempt |
| GET topic/:slug/practice/?page=1 | Distinct reviewed canonical questions from eligible branch; 50-question page |
| POST topic/:slug/practice/check/ | `{collection_id, page, revision_token, answers}`; current signed collection validation, stateless |
| POST topic/:slug/chat/ | `{message, preset?, history?, selected?, allow_related?: false}`; current note evidence only; true is rejected |

Answer maps use question ID keys and choice ID integer values. Unknown questions, cross-question choices, malformed IDs/types and stale review tokens are rejected predictably; no partial saved attempt. Chat selection includes current source ID/revision/text. See [AI_SYSTEM](AI_SYSTEM.md).

## Student feature gate and authentication

With STUDENT_FEATURES_ENABLED=false, **all** auth/learner handlers return constant 503 `learner_features_unavailable`, for guests/students/staff and malformed bodies, without reading learner records. With the gate true:

| Method/path | Payload/result |
|---|---|
| POST auth/register/ | `{username,email,password,name?}`; normalized unique identity, validated password; authenticated session |
| POST auth/login/ | `{username,password}`; username or email, generic invalid credentials |
| POST auth/logout/; GET auth/status/ | End session; own identity only |
| POST auth/password-reset/ | `{email}`; generic 202 regardless of existence/delivery; invalid global origin configuration returns 503 for all |
| POST auth/password-reset/confirm/ | `{uid,token,password}`; single-use, 30-minute token; invalidates old sessions by password hash |
| POST auth/google/start/ | CSRF-protected; server-session state/nonce/PKCE and consent URL; 503 if unconfigured |
| GET auth/google/callback/?state=...&code=... | Validated one-use callback; no tokens retained, no implicit account linking; redirect /dashboard |

No client-accessible mock-login shortcut exists. External OAuth/token exchange is mocked in tests. Auth rate windows store HMAC keys/counters, not raw credentials/IP/email. Legacy users remain users; no ownerless learning data is assigned during login.

## Owned learning and planning

| Method/path | Payload/result |
|---|---|
| GET dashboard/, bookmarks/, progress/, profile/weaknesses/ | Authenticated user's records only; publication-aware live learning; snapshot-based practice history |
| POST topic/:slug/bookmark/ | Exactly `{is_bookmarked: boolean}`; idempotent own add/remove |
| POST topic/:slug/progress/ | Exactly `{is_completed: boolean}`; published learning unit only |
| POST topic/:slug/visit/ | Empty object; explicit visit, does not change completion; reading GET never writes |
| GET/POST plans/ | Own plan list / create |
| GET/POST plans/:id/ | Own plan detail / edit with matching integer revision |
| POST plans/:id/reschedule/ | `{revision,start_date}`; retain completed task history |
| POST plans/:id/tasks/:task_id/ | Exactly `{is_completed: boolean}`; owned plan, eligible lesson |
| POST topic/:slug/quiz/submit/ | Signed quiz payload plus UUID submission_id; owned immutable snapshot |
| POST topic/:slug/practice/submit/ | Signed collection payload plus UUID submission_id; owned immutable snapshot |
| GET attempts/?page=1, attempts/:id/ | Own paginated history/detail; other users receive 404 |

Plan creation requires exactly title, mode (`learn`/`revision`), study_days (unique integers 0=Monday…6), daily_minutes (15–720), default_estimate_minutes (15–2400), start_date (YYYY-MM-DD), exam_date (date/null), topic_ids (1–250 distinct existing published IDs). Edit additionally requires revision; conflicts return 409. Derived daily/weekly/monthly tasks use the shared published-learning-unit rule. Generation bounds: two years/5,000 tasks. Completed task IDs/timestamps survive regeneration.

Submit retries with the same user/UUID and identical payload return the same saved attempt; changed payload returns 409. Guests must use stateless check. Snapshot text/choices/explanations/scores/classification survive later canonical edits/deletions. Legacy attempts have an empty snapshot and honestly report detailed history unavailable.

All learner queries filter request.user; URL IDs are ownership-checked. Current publication/review is revalidated on mutations. Admin endpoints remain separate, staff-only, with superuser account management. [Security](SECURITY.md), [schema](DATABASE_SCHEMA.md), [testing](TESTING.md).

## Account deletion readiness (policy pending)

GET /api/account/deletion/: when learners enabled and authenticated,200 with status=policy_approval_required, deletion_enabled=false and only caller-owned bookmark/progress/attempt/plan/task counts. POST accepts only password and confirmation=DELETE MY ACCOUNT; authenticated session, CSRF and rate limits required. Wrong/unsupported password403, unknown fields400, missing confirmation400, valid request409 deletion_policy_pending. No deletion/request queue is persisted. DELETE405; guest401; when learners closed all methods503 learner_features_unavailable before authentication/body/DB queries. Irreversible account deletion awaits owner-approved retention/session/backup policy; no frontend delete action is advertised.
