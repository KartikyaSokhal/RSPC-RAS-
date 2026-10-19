# Database and Migration Boundary — PREPAL 1.0

## 1. Baseline Preservation & Integrity
Original models and migrations 0001–0004 are preserved: `Topic`, `ContentBlock`, `Quiz`, `Question`, `Choice`, `Bookmark`, `UserProgress`, `QuizAttempt`.
- Real SQLite database path: `backend/db.sqlite3`
- Verified SHA-256 hash: `035bb88637e77ff361dab75c0d4cf80db0a6220f270870a18929be2c3ba313e4` (100% intact).
- Existing records have no inferred ownership and remain isolated as legacy records (`user=None`).

## 2. Additive Migrations

### Migration `0005_mvp_publication_resources_budget.py`
Created editorial snapshots and safety infrastructure:
- `TopicPublication`: Versioned JSON snapshots of approved topic content blocks, revision history, and publication timestamps.
- `TopicRelation`: Directed related/prerequisite links between curriculum topics.
- `LearningResource`: Private PDF candidates, file hash, page count, and rights metadata.
- `ResourcePage`: Page-level extracted text and citation anchors.
- `QuizReview`: SHA-256 content fingerprint binding review approval to exact questions and choices.
- `AiBudgetBucket` & `AiRequest`: Strict token, spend, and request rate limiting.

### Migration `0006_learner_ownership.py` (New in PREPAL 1.0)
Introduces user ownership to enable student authentication and private progress tracking:

| Model | Added Field | Added Constraint | Purpose |
|---|---|---|---|
| `Bookmark` | `user = ForeignKey(User, null=True, blank=True, on_delete=CASCADE)` | `UniqueConstraint(fields=['user', 'topic'], condition=Q(user__isnull=False))` | Associates saved topics with an individual student; prevents duplicate bookmarks per student. |
| `UserProgress` | `user = ForeignKey(User, null=True, blank=True, on_delete=CASCADE)` | `UniqueConstraint(fields=['user', 'topic'], condition=Q(user__isnull=False))` | Tracks completed curriculum topics per student; preserves legacy progress as unowned (`user=None`). |
| `QuizAttempt` | `user = ForeignKey(User, null=True, blank=True, on_delete=CASCADE)` | N/A (multiple attempts permitted per student) | Saves individual practice test scores, attempt timestamps, and question-level responses. |

## 3. Migration Safety Rules & Verification
- **Isolated Testing**: Migration `0006_learner_ownership.py` was tested and applied on `.local/demo/demo.sqlite3` and the in-memory test database runner. All 62 Django tests pass.
- **Copy Verification**: Forward migration preserves all existing rows and sequence numbers.
- **Legacy Record Isolation**: Queries for authenticated students filter strictly by `user=request.user`. Legacy records (`user=None`) are never exposed or reassigned to new users.
- **Production Gate**: Migration `0006` has **not** been applied to the real database `backend/db.sqlite3`. Applying this migration to production requires explicit owner approval and a verified pre-migration backup.
