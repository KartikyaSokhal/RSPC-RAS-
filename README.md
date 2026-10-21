# Prepal — content-first RPSC/RAS preparation

React 19/Vite with Django 6/DRF and Django Admin. PostgreSQL is the normal application database; the original SQLite archive and existing demos are preserved. Public syllabus, published notes, reviewed resources, approved topic connections/tags and stateless MCQ practice are implemented. Student accounts, dashboards, bookmarks, progress and saved attempts remain disabled.

## Current release boundary

Branch `codex/prepal-1-0`, HEAD `49407b2dcbf94a7d255bbc702afe039071ff65e7`. Documentation cleanup is local and uncommitted: 12 archived document removals and 16 approved edits, yielding 211 release files and 19 Markdown documents. No application/model/migration/dependency change. Publication remains blocked pending owner review; no commit, push, merge or deployment is authorized. [Status](docs/PROJECT_STATUS.md), [verification](docs/TESTING.md) and [handoff](docs/AGENT_HANDOFF.md) record current evidence and next steps.

The audited GitHub main still contains a retired development key in its settings; current local code omits it. Local rotation remains intact. Real environment files were not tracked in inspected Git history; only safe templates were found. Do not deploy the old main tree or restore historical credentials. See [security](docs/SECURITY.md).

## Install

Use the pinned versions in [.nvmrc](.nvmrc) and [.python-version](.python-version). From the application root:

```sh
npm ci
python3.14 -m venv backend/.venv
backend/.venv/bin/python -m pip install --require-hashes -r backend/requirements-dev.txt
```

Keep credentials in ignored private configuration. [Backend setup](backend/README.md), [database schema](docs/DATABASE_SCHEMA.md) and [safe environment template](backend/.env.example) describe PostgreSQL configuration. Normal settings refuse implicit SQLite fallback or the original archive path. This documentation cleanup authorizes no migration or cutover.

## Academic sample demo — 21 October 2026

The existing `.local/sample-content-v1` demo has five subjects/142 original topics, 15 original lessons (428–480 words each), 75 MCQs/300 choices, 19 tags, 15 aliases and 30 approved links/relations. Thirty publications include lessons and required ancestors. Each subject pool contains 15 distinct questions. These are non-production engineering fixtures, not independent academic approval; no learner/AI usage rows were seeded.

Run the ALREADY PREPARED demo in one terminal:

```sh
export PREPAL_DEMO_ROOT="$PWD/.local/sample-content-v1"
PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/manage.py runserver 127.0.0.1:8000 --settings=core.demo_settings
```

In a second terminal:

```sh
PREPAL_API_ORIGIN=http://127.0.0.1:8000 npm run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173` or `/topic/a-temples`. This explicit SQLite demo needs no PostgreSQL server and uses the mock Tutor. Existing Admin credentials remain private inside that demo directory. Do not publish or reuse them. The [catalogue](docs/ADMIN_WORKFLOW.md#local-academic-sample-content--21-october-2026) and [versioned corpus](backend/content/fixtures/sample_lessons_v1.json) contain lesson/source details.

For FUTURE separately authorized demo reproduction, `scripts/prepare_sample_demo.py --directory <new-private-directory>` creates a new database using existing migrations and refuses every existing destination. Do not execute it during this no-migration cleanup. Preserve failed/manual demos. Set PREPAL_DEMO_ROOT to an existing isolated sample and run `scripts/verify_sample_demo.py` with the backend interpreter for query-only verification.

## Checks and operation

```sh
npm run check
backend/.venv/bin/python backend/run_tests.py
PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/manage.py check --settings=core.test_settings
backend/.venv/bin/python scripts/check_docs.py --release
backend/.venv/bin/python scripts/release_manifest.py
```

Tests use isolated configurations and mocked AI. [TESTING](docs/TESTING.md) covers optional browser/PostgreSQL checks and their safeguards. `scripts/release_manifest.py --export /absolute/new/private-directory` creates a verified worktree copy without private data or Git mutation. Open `prepal.code-workspace` for shared IDE exclusions; installed dependencies remain local.

Published snapshots separate draft edits from public content. PDFs need explicit text/rights review; raw private-media URLs are closed. Uploaded-PDF reading is implemented; topic-note PDF export and strict current-topic-only Tutor are pending Phase C. Current Tutor may opt into reviewed related sources and is default-off for live requests. No live Gemini quality/billing claim, production target/domain, real cutover or deployed URL is established. Use [roadmap](docs/IMPLEMENTATION_PLAN.md), [deployment gates](docs/DEPLOYMENT.md) and [documentation index](docs/README.md).

## License

All rights reserved. Educational and architectural materials prepared for RPSC/RAS preparation.
