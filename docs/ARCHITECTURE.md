# Implemented Architecture — PREPAL 1.0

## 1. System Topology & Technology Stack
- **Frontend**: React 19 (SPA) with Vite. Modular architecture with lazy-loaded routes and PDF worker chunks. Vanilla CSS design system with CSS custom properties (`tokens.css`, `App.css`). No heavy component or animation frameworks.
- **Backend**: Django 5.x on Python 3.12 with Django REST Framework. SQLite database with WAL mode and 5-second lock timeout.
- **Development & Production Proxies**: In development, Vite proxies `/api` to Django loopback (`127.0.0.1:8000`). In production, Nginx or Cloudflare serves static assets from `dist/` and forwards `/api`, `/admin`, and `/static` to Gunicorn/Uvicorn.
- **State & Session Persistence**: Authentication uses Django's secure, HTTP-only session cookies (`sessionid` and `csrftoken`). No auth tokens are stored in browser `localStorage`. Theme preference (`light`/`dark`) is the only state persisted client-side.

## 2. Authentication & Student Ownership Architecture
- **Session Auth**: Endpoints `/api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`, and `/api/auth/status/` manage student identities using Django's built-in `django.contrib.auth`.
- **Model Ownership**:
  - `Bookmark`, `UserProgress`, and `QuizAttempt` models include a nullable `user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)`.
  - Conditional constraints (`UniqueConstraint(fields=['user', 'topic'], condition=Q(user__isnull=False))`) ensure single-user uniqueness while preserving legacy records (`user=None`).
  - All learner endpoints strictly filter by `user=request.user` when authenticated, preventing any cross-user data leakage.
- **Unauthenticated Guests**: Public syllabus browsing, note reading, and search remain 100% accessible to unauthenticated guests without leaking or writing to shared records.

## 3. Search Engine Architecture
- **In-Memory SQLite Search (`content/services/search.py`)**:
  - Searches all 152 discoverable syllabus topics, verified notes, and approved PDFs.
  - Normalizes whitespace and executes case-insensitive partial word queries.
  - Generates typo tolerance suggestions using Python's standard `difflib.get_close_matches(word, vocabulary, cutoff=0.72)`.
  - Draft note bodies and unapproved PDFs are strictly excluded from search querysets.

## 4. Student Dashboard & Deterministic Progress
- Endpoint `/api/dashboard/` evaluates user-scoped progress:
  - Progress percentage: `(completed_topics / total_topics) * 100`.
  - Saved bookmarks count and list.
  - Quiz attempts history with scores and timestamps.
  - Deterministic suggested next topics: analyzes uncompleted topics within current streams without inventing synthetic "AI mastery scores".

## 5. RAG & AI Tutor Safety Controls
- **Scoped Retrieval**: `DatabaseRetrievalProvider` retrieves only the current lesson text, approved PDF pages, and up to two explicitly linked prerequisite/connected topics with opt-in.
- **Budget & Quota Reservations**: Pre-allocated spend caps and per-session rate limits prevent runaway API billing.
- **Answer Integrity**: Real source citations are validated against a server manifest; invalid or out-of-scope citations fail closed.

## 6. Schema Migrations & Isolation
- Schema migration `0006_learner_ownership.py` is purely additive.
- Tested and verified on copy `.local/demo/demo.sqlite3` and in-memory test runner.
- Production database `backend/db.sqlite3` remains on its verified baseline until owner approval.
