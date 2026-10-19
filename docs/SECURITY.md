# Security Boundaries and Release Conditions — PREPAL 1.0

## 1. Resolution of P002 (Safe Learner State & Ownership)
- **Problem in P002**: Previously, bookmarks and progress records lacked user ownership, resulting in a single shared state across all users. As a temporary containment, learner endpoints returned 503.
- **Permanent Architectural Resolution**:
  - `user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)` added to `Bookmark`, `UserProgress`, and `QuizAttempt`.
  - Conditional constraints (`UniqueConstraint(fields=['user', 'topic'], condition=Q(user__isnull=False))`) enforce unique bookmarks and completion records per student.
  - Every learner queryset strictly filters by `user=request.user`.
  - Legacy records (`user=None`) remain completely isolated and are never exposed or reassigned.
  - Cross-user data leakage is prevented by design; verified with automated multi-user isolation tests in `test_auth.py`.
- **Public & Guest Protection**:
  - Unauthenticated guests can browse the complete syllabus, search all discoverable topics, read verified notes, and practice untimed quizzes.
  - Guest bookmark or progress actions prompt the user to sign in and never write shared records to the database.

## 2. Authentication & Session Security
- **Django Session Auth**: Uses Django's battle-tested session framework with HTTP-only cookies (`sessionid` and `csrftoken`).
- **No Token Storage in LocalStorage**: Prevents JWT theft via XSS/script injection.
- **CSRF Protection**: All state-mutating requests (`POST`, `PUT`, `DELETE`) require a valid `X-CSRFToken` header matching the session cookie.
- **Password Validation**: Minimum 8 characters, common password checks, and secure PBKDF2/Argon2 hashing.

## 3. Rendering Boundaries (P001 Retention)
- **Browser Boundary**: DOMPurify educational allowlist sanitizes all rendered lesson HTML; raw HTML in Markdown is disabled for model outputs.
- **Server Boundary**: Publication snapshots sanitize rich text with `nh3`, stripping executable scripts, iframes, inline event handlers, and untrusted protocols.
- **Image & PDF Assets**: Hash-checked URLs; raw storage paths are never exposed to clients.

## 4. Search & Content Boundaries
- **Draft Isolation**: Global search queries all 152 discoverable syllabus topics, verified notes, and approved PDFs. Unpublished draft content blocks and private PDFs are strictly excluded from search querysets.
- **Typo Tolerance**: Python `difflib` suggestions operate only on approved curriculum vocabulary, preventing extraction of private terms.

## 5. RAG & AI Safety Controls
- **Scoped Grounding**: AI responses are strictly grounded in verified lesson notes and approved source PDFs.
- **Cost & Quota Controls**: Hard spend caps and request reservations prevent budget exhaustion.
- **Model Isolation**: Mock demo settings prevent accidental live Gemini API credit consumption during local development and testing.

## 6. Pre-Production Security Checklist
- [ ] Explicit owner approval and verified backup prior to applying migration `0006` on `backend/db.sqlite3`.
- [ ] Verify `DEBUG = False`, `ALLOWED_HOSTS`, and `SECURE_SSL_REDIRECT` in production settings.
- [ ] Configure live Gemini API key and daily spend limits.
- [ ] Set trusted proxy headers (`X-Forwarded-Proto`) behind reverse proxy.
