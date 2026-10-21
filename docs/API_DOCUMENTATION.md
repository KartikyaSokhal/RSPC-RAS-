# Phase 3 current public discovery API

All responses use current publication eligibility and Cache-Control: no-store. GET never invokes AI, inserts links into stored HTML or creates learner/quiz records.

| Route | Method / behavior |
|---|---|
| `/api/topic/<slug>/` | Existing reader payload plus `keyword_links` (up to 8 source-bound approved spans with target cards), public `tags`, and deduplicated `related` (up to 6) |
| `/api/topic/<slug>/context/` | GET current published title/description/path; 404 when withdrawn/unavailable. Used on popup open, with no draft fallback |
| `/api/tags/<slug>/?page=1` | GET explicitly public tag; released published article cards, syllabus paths/read_minutes, count/page/page_size 30. Empty known tags return 200/empty results; unknown/private tags 404 |
| `/api/topic/<slug>/practice/?page=1` | GET reviewed canonical branch collection: collection_id, title, questions/choices (no answer key), page/page_size 50/count, signed revision_token. Empty/unavailable 404 |
| `/api/topic/<slug>/practice/check/` | CSRF-protected POST with exactly collection_id, page, revision_token, answers. Returns shared deterministic score/explanations, without attempts or learner records |

Page parameters must be one decimal number 1–250. Check requests require integer IDs/page and strict answer formats; malformed/membership requests return 400, expired/changed/tampered manifests 409, unavailable collections 404. Tokens bind collection/page/question IDs, quiz review hashes and primary publication revisions and expire after one hour. Existing legacy quiz endpoints and all disabled learner endpoints remain unchanged.

Keyword data uses stable block IDs, text-node indexes and UTF-16 offsets; the client verifies exact text after sanitization and fails closed on repaired/mismatched markup. Popup URLs are constructed local routes, never AI/authored HTML attributes. Earlier Phase 2 text below records the prior API boundary, superseded by this section.


# Phase 2 API compatibility

No new public tag, alias, collection or dynamic-link endpoint is introduced. Existing reader/search/resource/practice payloads retain their shape; draft tag/alias metadata is not exposed through raw content. Internal `services.collections.question_collection(topic)` returns canonical distinct question records with reviewed/publication eligibility by default; only Admin uses its draft-inclusive mode. Approved relationship status is checked by the central publication resolver. Stateless grading and every disabled learner/auth route remain unchanged. See [schema](DATABASE_SCHEMA.md) and [Admin workflow](ADMIN_WORKFLOW.md).

# Phase 1 API contracts

API root `/api/`. Service errors use `{ "error": { "code": "...", "message": "..." } }`; relevant public and unavailable responses have `Cache-Control: no-store`.

## Content-first learner boundary

The following paths always return HTTP 503 with `learner_features_unavailable` for GET/HEAD/POST/PUT/PATCH/DELETE, independent of guest/student/staff/superuser identity, credentials, body validity or CSRF. Unsupported methods retain DRF's normal method handling. These handlers do not evaluate credentials or read/write learner records.

- `auth/register/`, `auth/login/`, `auth/logout/`, `auth/status/`
- `dashboard/`, `bookmarks/`, `progress/`, `profile/weaknesses/`
- `topic/<slug>/bookmark/`, `topic/<slug>/progress/`, `topic/<slug>/quiz/submit/`

Example: `{ "error": { "code": "learner_features_unavailable", "message": "Student accounts and personalized features are unavailable in this content-first release. Reading and stateless practice remain available." } }`.

This constant read-only failure needs no CSRF. Functional guest POST operations below remain CSRF protected. `/admin/login/` and `/admin/logout/` use Django's normal administrative session/CSRF handling. An unavailable `/api/auth/logout/` does not end an administrative session.

## Enabled public API

| Method/path | Contract |
|---|---|
| GET `health/` | Database/publication schema readability; returns status ok, not a content-readiness claim |
| GET `config/` | Demo flag, tutor availability, CSRF initialization and signed visitor cookie |
| GET `topics/?tree=1` | Configured syllabus hierarchy; `published_only=1` limits to eligible snapshots |
| GET `topic/<slug>/` | Published content/resources/relations or safe coming-soon outline; never raw draft blocks |
| GET `search/?q=...&page=1` | Discoverable titles, eligible note/PDF snippets and typo suggestion; bounded input/page |
| GET `resources/<id>/?page=1` | Eligible resource metadata and extracted page text |
| GET `resources/<id>/file/` | Hash-checked approved PDF referenced by a current publication |
| GET `topic/<slug>/images/<block_id>/` | Current snapshot's hash-checked image |
| GET `topic/<slug>/quiz/?quiz_id=<id>` | Reviewed quiz/choices, stable ID and expiring revision token; no answer keys |
| POST `topic/<slug>/quiz/check/` | CSRF + `{quiz_id, revision_token, answers}`; +1 correct / 0 wrong/unanswered; no persistence |
| POST `topic/<slug>/chat/` | CSRF, bounded message/history/selection, source-scoped response; 503 when disabled |

Every `is_bookmarked` and `is_completed` value is false for every identity; no learner query is made during serialization. `/private-media/` and `/media/` have no public Django route. Raw legacy attachment URLs are not returned as usable public files.

Review fingerprints, not `APPROVED_QUIZ_IDS`, determine quiz eligibility in the current implementation. No quiz generation/provider call occurs during GET. Stateless checking remains available to guests and users already holding an administrative or historical session.
