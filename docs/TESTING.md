# Reproducible Verification — PREPAL 1.0

## Test Suite Execution Commands

```sh
# 1. Frontend Lint, Unit Tests & Production Build (Vitest & Vite)
npm run check

# 2. Django Backend Test Suite (Isolated Memory Runner)
backend/.venv/bin/python backend/run_tests.py content

# 3. Playwright E2E Browser Test Suite (Chromium)
npx playwright test

# 4. Screenshot Gallery & Visual Verification
node scripts/capture_gallery.mjs
backend/.venv/bin/python scripts/build_gallery.py

# 5. Documentation Target Link Verification
backend/.venv/bin/python scripts/check_docs.py
```

## Current Test Results

| Test Suite | Total Tests | Passing | Failing | Description |
|---|---|---|---|---|
| **Django Backend** | 62 | 62 (100%) | 0 | Model ownership, student registration/auth/logout, CSRF protection, multi-user isolation, user-scoped bookmarks/completion/quizzes, search with difflib typo suggestions, publication snapshots, RAG budget safety, and PDF extraction boundaries. |
| **Vitest Frontend** | 59 | 59 (100%) | 0 | Content block rendering, DOMPurify security, sanitized HTML/Markdown, simplified navbar, light/dark theme toggle, search suggestions/tags, login/signup form validation, student dashboard guest prompts, and topic action buttons. |
| **Playwright E2E** | 8 | 8 (100%) | 0 | Chromium browser interactions: catalog navigation, topic reader, student account prompts, stateless quiz checking, untimed quiz UI, sanitized active HTML rejection, and grounded tutor conversation. |
| **ESLint & Vite Build** | — | Clean (0 err, 0 warn) | 0 | Strict lint rules, zero cascading-render warnings, full production bundle compilation in under 1 second. |
| **Visual Gallery** | 27 screenshots | 27 verified | 0 | Browser-rendered full-page screenshots of desktop/mobile viewports, dark/light modes, Rajasthan map hero, search with suggestions, auth pages, and student dashboard. |

## Database Safety Verification
- Real SQLite database path: `backend/db.sqlite3`
- Verified SHA-256 hash: `035bb88637e77ff361dab75c0d4cf80db0a6220f270870a18929be2c3ba313e4`
- Confirmed zero mutations to the real database during all development, test runs, and screenshot generation.
