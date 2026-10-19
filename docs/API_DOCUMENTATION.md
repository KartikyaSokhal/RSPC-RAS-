# Current API Contracts — PREPAL 1.0

All routes are under `/api/`; public responses use `Cache-Control: no-store`. Standard error responses use `{ "error": { "code": "...", "message": "..." } }`. Unauthenticated requests retain full public reading access.

## 1. Authentication Endpoints

| Method / Path | Auth Required | Request Payload | Response | Behavior |
|---|---|---|---|---|
| POST `auth/register/` | No | `{ "username": "...", "password": "...", "email": "...", "name": "..." }` | `{ "authenticated": true, "user": { "id": 1, "username": "...", "name": "..." } }` | Creates student account, starts session, sets session cookies. Password must be ≥ 8 chars. |
| POST `auth/login/` | No | `{ "username": "...", "password": "..." }` | `{ "authenticated": true, "user": { ... } }` | Authenticates credentials, rotates CSRF, establishes session. |
| POST `auth/logout/` | Yes | `{}` | `{ "authenticated": false, "message": "Logged out." }` | Flushes session cookies. |
| GET `auth/status/` | No | None | `{ "authenticated": bool, "user": {...} \| null }` | Returns current session authentication state and user profile. |

## 2. Student Dashboard & Learner Endpoints

| Method / Path | Auth Required | Request / Query | Response | Behavior |
|---|---|---|---|---|
| GET `dashboard/` | Yes | None | `{ "stats": { "total_topics": 152, "total_completed": n, "progress_percentage": n, "total_bookmarks": n, "total_quizzes_taken": n }, "bookmarks": [...], "completed_topics": [...], "quiz_attempts": [...], "suggested_next": [...] }` | User-scoped progress metrics, bookmarks, completion list, quiz history, and deterministic suggestions. |
| GET `bookmarks/` | Yes | None | `[ { "id": 1, "topic": { "slug": "...", "title": "..." }, "created_at": "..." } ]` | Lists all bookmarks owned by the authenticated student. |
| POST `topic/<slug>/bookmark/` | Yes | `{}` | `{ "is_bookmarked": bool, "message": "..." }` | Toggles bookmark for current student. 401 if unauthenticated. |
| GET `progress/` | Yes | None | `[ { "id": 1, "topic": { "slug": "...", "title": "..." }, "completed": bool } ]` | Lists all topic completion records for current student. |
| POST `topic/<slug>/progress/` | Yes | `{ "completed": bool }` (optional) | `{ "is_completed": bool, "message": "..." }` | Toggles topic completion for current student. 401 if unauthenticated. |
| POST `topic/<slug>/quiz/submit/` | Yes | `{ "quiz_id": 1, "revision_token": "...", "answers": { "1": 2 } }` | `{ "score": 100, "total": 1, "attempt_id": 1, "results": [...] }` | Evaluates answers, records owned `QuizAttempt`, returns question-level explanations. |

## 3. Public Discovery & Reading Endpoints

| Method / Path | Auth Required | Behavior |
|---|---|---|
| GET `health/` | No | `{ "status": "ok" }` when publication schema/database is readable. |
| GET `config/` | No | Feature flags (`demo`, `ai_enabled`), CSRF token. |
| GET `topics/?tree=1` | No | Returns full 152-topic syllabus hierarchy. If authenticated, annotates each node with `is_bookmarked` and `is_completed`. |
| GET `topic/<slug>/` | No | Approved blocks, revision, breadcrumbs, children, related links, resources. Annotates with student's `is_bookmarked` and `is_completed` if authenticated. |
| GET `search/?q=...&page=1` | No | Searches all 152 discoverable topics, published notes, and approved PDFs. Returns `{ "total": n, "results": [...], "suggestion": "..." }` with typo tolerance. |
| GET `resources/<id>/?page=1` | No | Approved published resource metadata, extracted page text, authorized file URL. |
| GET `resources/<id>/file/` | No | Hash-checked PDF stream only while approved and referenced by published topic. |
| GET `topic/<slug>/quiz/?quiz_id=<id>` | No | Reviewed quiz structure, ordered questions/choices, expiring revision token. No answers leaked. |
| POST `topic/<slug>/quiz/check/` | No | CSRF + revision token; stateless read-only grading and explanations for guests. |
| POST `topic/<slug>/chat/` | No | CSRF + visitor cookie; scoped RAG answering grounded in lesson sources and approved PDFs. |
