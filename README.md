# Prepal — remediated Phase A release baseline

Branch `codex/prepal-1-0`; verification/base HEAD `ee272a6954868b303447545eb553200adb024a24`. The owner approved the local commit **Prepare Prepal content-first MVP release baseline**, conditional on security remediation and verification. The release commit is the commit containing this update; resolve its full SHA with `git log -1 --format=%H -- docs/AGENT_HANDOFF.md`. No push, deployment or real database cutover is authorized.

The exposed historical Django key was confirmed active only in ignored local development configuration, then replaced atomically with a new cryptographically random key. No old-key fallback remains. Old local sessions/reset links/signed cookies/practice tokens expire; reauthenticate or reload practice. Passwords, content, original/demo databases and media were not changed. Production credentials were not accessed or rotated. The inactive key remains in two historical commits, including the commit currently on GitHub main; history was not rewritten. Remote visibility/external credential reuse remain unverified, so provision independent fresh production secrets.

Fresh verification: **80 frontend tests**, lint/build, **121 backend tests plus four PostgreSQL skips**, and **nine rotation checks** passed. Gitleaks v8.30.1 found no findings in staged/full-index/history scans; separate exact-value checks identify the known retired historical key and no exposed current local credentials. See [security](docs/SECURITY.md), [verification](docs/TESTING.md) and [handoff](docs/AGENT_HANDOFF.md). The staged tree matches all **223 release inputs**, excluding private data/credentials/output. Phase B requires separate push approval; Phase C PDF export/current-topic Tutor and subsequent production work remain pending. Dated setup/history below is retained.

---

# Controlled local cleanup and release preparation

The application checkout is `Prepal/` on `codex/prepal-1-0`, unchanged HEAD `ee272a6954868b303447545eb553200adb024a24`. Current Phase 1–4/sample implementations remain uncommitted. Open `prepal.code-workspace` for the application-only IDE view. Shared exclusions hide installed dependencies, private runtime data and generated output without deleting required dependencies.

Retired Express/Mongo source and the obsolete `backend/env` were privately archived after a verified recovery snapshot. Use `backend/.venv`; neither archived environment nor Node backend belongs in startup/deployment. Original SQLite, all existing demos/media, migrations 0001–0008, historical evidence and dormant learner code remain protected.

Use the pinned Node/Python versions and install from locks in a new checkout:

```sh
npm ci
python3.14 -m venv backend/.venv
backend/.venv/bin/python -m pip install --require-hashes -r backend/requirements-dev.txt
npm run check
backend/.venv/bin/python backend/run_tests.py
backend/.venv/bin/python scripts/check_docs.py --release
backend/.venv/bin/python scripts/release_manifest.py
```

`release_manifest.py --export /absolute/new/private-release-copy` creates a hash-verified copy of explicit source/config/test/canonical-document inputs; it never stages, commits, copies private databases/credentials or changes remotes. The exported manifest includes current uncommitted inputs and is not a published Git revision. Canonical docs are trackable; historical archives remain private and are referenced as archival identifiers rather than broken checkout links. The checker detects excluded Markdown targets with `--release`.

Current local verification: **80 frontend tests, 121 backend tests (four PostgreSQL-only skips), 28 Chromium tests and 97 sample API checks passed**; lint/build and 29 automated accessibility scans passed. Fresh dependencies installed successfully in the disposable 223-input release export. No published clean Git commit or remote CI run is claimed.

Start the isolated sample with the commands below; they need no PostgreSQL server. Normal application settings require explicitly configured PostgreSQL. Local cleanup does not complete Phase 5, live Gemini evaluation, topic-note PDF export, a real database cutover or public deployment. [Current results](docs/TESTING.md), [release status](docs/PROJECT_STATUS.md) and [handoff](docs/AGENT_HANDOFF.md) define the verified boundary.

---

# Prepal — content-first RPSC/RAS MVP

React 19/Vite + Django 6/DRF + Django Admin, with PostgreSQL as the required primary database. Phase 3 provides reviewed dynamic phrase links/popups, related topics, approved tag pages and canonical syllabus practice. Phase 4B adds the targeted frontend improvements: numbered expandable syllabus, data-driven subject navigation/counts, Search/theme header, compact map hero and one responsive Tutor launcher. The real SQLite archive remains unchanged; real cutover and public deployment require separate approval.

## Release boundary

Available: syllabus browsing, published notes, topic navigation, reviewed MCQ retrieval, stateless checking, approved PDFs, source-restricted tutor when explicitly enabled, and administrative authoring/review/publication.

Deferred: public student registration/login, dashboards, bookmarks, progress, saved attempts, personalized plans and student reports. Disabled APIs return 503 `learner_features_unavailable` for every identity. Administrative staff login remains functional. Historical models, data and dormant implementation are retained.

Source content has 142 topics and six blocks; the 152-topic demo adds synthetic methodology fixtures. Code/test approval does not establish editorial review of the real syllabus corpus. Homepage/footer/full-syllabus statistics reflect the actual hierarchy response; search copy no longer hardcodes demo totals. Loading/errors never invent counts, and successful empty data remains zero.

## Academic sample demo — 21 October 2026

A separate demo is ready at `.local/sample-content-v1/demo.sqlite3`: the original **142-topic/five-subject hierarchy**, **15 lessons** (428–480 note words each; 6,754 total), **75 reviewed sample MCQs/300 choices**, **19 reused controlled tags**, **15 aliases** and **30 approved inline/related connections**. Thirty topic publications comprise 15 lessons and 15 necessary ancestor containers. Each subject has 15 distinct questions; no learner records or AI requests are seeded. The original SQLite and both previous demos remain unchanged.

The corpus is [sample_lessons_v1.json](backend/content/fixtures/sample_lessons_v1.json), with 28 verified reference URLs and original wording. Notes and quiz reviews explicitly identify non-production sample material. Review status enables local feature testing; it does not represent independent human academic approval. No external articles, images or PDFs are copied into this sample database.

Run the **already prepared** demo from the application root in one terminal:

```sh
export PREPAL_DEMO_ROOT="$PWD/.local/sample-content-v1"
PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/manage.py runserver 127.0.0.1:8000 --settings=core.demo_settings
```

In a second terminal, from the same application root:

```sh
PREPAL_API_ORIGIN=http://127.0.0.1:8000 npm run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`, then Explore Syllabus, or start at `/topic/a-temples`. PostgreSQL/psql is not required for this explicitly isolated SQLite demo. AI stays on the existing mock provider. Private Admin credentials are in `.local/sample-content-v1/admin-credentials.txt`; never publish or reuse them.

To reproduce in a **new** directory (never run a reset on an existing demo):

```sh
backend/.venv/bin/python scripts/prepare_sample_demo.py --directory "$PWD/.local/sample-content-next"
PREPAL_DEMO_ROOT="$PWD/.local/sample-content-next" backend/.venv/bin/python scripts/verify_sample_demo.py
```

Preparation runs existing migrations 0001–0008 only against the new empty demo. It refuses any existing destination, including symlinks to existing directories. A failed preparation leaves its isolated directory for inspection; select another new directory instead of deleting data. Verification is read-only and intentionally fails if the versioned sample has been manually changed. [Lesson catalogue and review meaning](docs/ADMIN_WORKFLOW.md); [actual test results](docs/TESTING.md).

## Development setup

Use the versions in `.nvmrc` and `.python-version`. Install frontend with `npm ci`, create `backend/.venv`, then install `backend/requirements-dev.txt` with pip's `--require-hashes` option. Runtime/dev Python locks are pinned; psycopg's binary driver is included. Regenerate locks with the documented commands in [backend README](backend/README.md).

For PostgreSQL development, create a new empty local database and provide the private POSTGRES_* environment described in [database setup](docs/DATABASE_SCHEMA.md) and [environment example](backend/.env.example). No real credentials are included. Only for a verified new disposable development database, apply schema migrations, then run:

```sh
backend/.venv/bin/python backend/manage.py runserver 127.0.0.1:8000
npm run dev
```

Normal settings require PostgreSQL and refuse an implicit fallback or the original SQLite path. Real data import uses the reviewed rehearsal/cutover procedure, not an automatic startup migration.

For a separate synthetic SQLite demo/mock tutor:

```sh
# Set PREPAL_DEMO_ROOT to a NEW private directory to preserve any existing demo.
backend/.venv/bin/python scripts/prepare_demo.py
backend/.venv/bin/python backend/manage.py runserver 127.0.0.1:8000 --settings=core.demo_settings
npm run dev
```

Preparation refuses an existing demo DB. Demo credentials are written privately inside the selected demo directory; do not reuse them for production. The real database and backend/.env are not used by this path.

## Verification and migration

```sh
npm run check
backend/.venv/bin/python backend/run_tests.py
# Explicit local disposable PostgreSQL environment required; see docs/TESTING.md.
backend/.venv/bin/python backend/run_tests.py --postgres
backend/.venv/bin/python scripts/verify_postgres_transfer.py
npm run test:e2e
# Prepare a NEW synthetic demo first, and use the same PREPAL_DEMO_ROOT.
npm run test:integration
```

Historical Phase 4B results: frontend 77/77, lint/build; Chromium 15 fixture tests and seven selected Django/mock student integration tests; 27 automated accessibility scans with zero violations. No backend tests or migrations ran in this frontend-only phase. Historical Phase 3 results: PostgreSQL 120/120; SQLite 116 passed/four PostgreSQL-only skips. Migration reversal and source-copy transfer preserve all 437 original rows/IDs/counters; PostgreSQL compares 34 tables and 32 sequences. [Actual verification and limitations](docs/TESTING.md). Earlier phase evidence remains historical.

## Authoring and security

Existing topic-tree/WYSIWYG editing, private previews, publish/withdrawal and quiz review remain. PDF preparation leaves resources ready for explicit text/rights review; it cannot approve or republish automatically. Raw private-media URLs are closed; historical ContentBlock attachment records remain stored but must use the reviewed resource workflow for public delivery. SafeHtml/Markdown and publication eligibility boundaries remain active.

AI is default-off; no live Gemini quality/billing claim is made. Production model/rates/cap, real corpus/rights review, TLS/roles/hosting, durable backups and target-host validation remain owner decisions. No real cutover, paid infrastructure, commit, push or deployment was performed.

Start with [status](docs/PROJECT_STATUS.md), [scope](docs/MVP_SCOPE.md), [implementation files](docs/IMPLEMENTATION_PLAN.md), [database/recovery](docs/DATABASE_SCHEMA.md), [Admin workflow](docs/ADMIN_WORKFLOW.md) and [documentation index](docs/README.md). Earlier scope/verification remains historical in CHANGELOG and docs/evidence. Next task: obtain the Phase 5 brief, acceptance criteria and approval; do not start Phase 5 implementation.

## License

All rights reserved. Educational and architectural materials prepared for RPSC/RAS preparation.
