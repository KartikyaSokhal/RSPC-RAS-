# Prepal — RPSC/RAS learning platform

Prepal connects the Rajasthan examination syllabus to published study notes, reviewed resources and practice questions. React 19/Vite provides the student interface; Django 6/DRF, Django Admin and PostgreSQL provide authoring, publication and owned student records.

## Features

- Hierarchical syllabus explorer, search, light/dark themes and responsive topic reading.
- Editorially approved keyword popups, related topics and controlled tag discovery.
- Reviewed canonical MCQs, deterministic grading and stateless guest practice.
- Session-based student accounts, owned bookmarks/completion, dashboard, recent reading and saved practice history.
- Deterministic study planning with approximate editor estimates, weekly/monthly targets and rescheduling that retains completed work.
- A single Tutor panel, restricted server-side to the current published lesson's notes, with source citations, refusals and cost controls.

These features are implemented and verified locally. Google OAuth is mocked in tests and needs owner credentials; password recovery needs configured SMTP. Live Gemini remains off and has not been called. Production student access defaults off until approved acceptance. Uploaded PDF reading is implemented; topic-note PDF export is deferred. There is no verified deployment URL or real database cutover.

## Install

Use [.nvmrc](.nvmrc) and [.python-version](.python-version). From this application root:

```sh
npm ci
python3.14 -m venv backend/.venv
backend/.venv/bin/python -m pip install --require-hashes -r backend/requirements-dev.txt
```

Normal runtime requires a separately provisioned PostgreSQL database and ignored private configuration based on [backend/.env.example](backend/.env.example). There is no automatic fallback to the original SQLite archive. See [backend setup](backend/README.md) and [deployment prerequisites](docs/DEPLOYMENT.md). Do not run migrations against existing valuable data without an approved backup/cutover plan.

## Isolated student review demo

Student UI is enabled only by the explicitly selected `core.student_demo_settings` environment. Normal development **and production** settings default `STUDENT_FEATURES_ENABLED=false`. The content-only `core.demo_settings` intentionally hides accounts; changing frontend buttons cannot bypass it.

For an **already prepared**, ready student-review database at schema 0012:

```sh
export PREPAL_DEMO_ROOT=/absolute/path/to/prepared/student-review
npm run dev:student -- --check
npm run dev:student
```

The guarded launcher starts Django on `127.0.0.1:8002` and Vite on `127.0.0.1:5173`. It reads the marker/schema without writing, refuses an unmarked/incomplete/original/symlinked database or production environment, and never prepares data or applies migrations. Stop conflicting local listeners before a cold start. Ctrl-C stops only its own child processes.

If Vite is already managed/running, set `PREPAL_DEV_API_ORIGIN=http://127.0.0.1:8002` in ignored `.env.local`, then run only the selected backend:

```sh
export PREPAL_DEMO_ROOT=/absolute/path/to/prepared/student-review
npm run dev:student -- --backend-only
```

Vite loads that override **only in development**, including when an old shell exports the previous API origin. Build/preview still use explicit PREPAL_API_ORIGIN or the usual fallback. This selects an API server, never enables accounts by itself; `/api/config/` and backend ownership/CSRF remain authoritative.

Open `http://127.0.0.1:5173/`. Logged out: Search, theme, Sign In, Sign Up. Logged in: Search, theme, Dashboard, named Account menu and Logout. The menu uses native keyboard controls; the existing routes are reused. No separate Profile page is invented. A guest opening /dashboard sees the sign-in prompt and cannot fetch private records.

Create a local student account. Recovery mail uses an in-memory test mailbox here, not delivered SMTP. Google remains a disabled, clearly unconfigured option. No real provider keys or paid AI requests are used. Existing Admin credentials stay private in the selected demo directory; do not publish or reuse them.

If no prepared environment exists, creating a NEW isolated sample requires separate authorization where migrations/preparation are restricted. The existing `scripts/prepare_student_demo.py --directory /absolute/new/private/directory` is the versioned preparation tool; it refuses existing destinations. Do not run it on the original archive or preserved demos merely to expose navbar controls. No preparation/migration was performed in this navigation task.

The demo includes the preserved versioned 15-lesson synthetic sample plus **25 new draft review lessons**, five per actual syllabus subject, with 125 new MCQs/500 choices. New academic material is not publicly published or quiz-approved. Its private `review-inventory.json` lists mappings, references and review states. See [Admin workflow/catalogue](docs/ADMIN_WORKFLOW.md) and [new corpus](backend/content/fixtures/student_lessons_v2.json). Human review/publication is required through the existing Admin; seed flags are never production approval.

Existing content-only demos continue to use `core.demo_settings`. Start already prepared demos without rerunning preparation or migrations. Original SQLite, demo data and private media remain preserved.

## Verify

```sh
npm run check
backend/.venv/bin/python backend/run_tests.py
backend/.venv/bin/python backend/manage.py check --settings=core.test_settings
backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
backend/.venv/bin/python scripts/check_docs.py --release
backend/.venv/bin/python scripts/release_manifest.py
```

[Testing](docs/TESTING.md) covers guarded disposable PostgreSQL, browser and clean-export checks. [Architecture](docs/ARCHITECTURE.md), [security](docs/SECURITY.md) and the [documentation index](docs/README.md) describe operational boundaries. Credentials, databases, media, dependencies and reports remain outside release inputs.

## License

All rights reserved. Independent examination preparation resource; not affiliated with RPSC or the government examination authority.

## PostgreSQL preparation and local recovery

The active student preview on8002 still uses the isolated SQLite student-review database; it has **not** been switched. A new disposable PostgreSQL16.2 rehearsal verified schema0001–0012, ownership, persisted sessions across backend restarts and encrypted independent restore. Normal PostgreSQL configuration uses separate migration/runtime/backup roles, bounded connections/timeouts and production verify-full TLS. Local rehearsals do not approve public student access.

Use [backend setup](backend/README.md), [deployment and recovery](docs/DEPLOYMENT.md), [security/retention approval](docs/SECURITY.md) and [verification](docs/TESTING.md). scripts/postgres_ops.py reads private0600 environment files; no passwords belong in shell arguments or Git. Account deletion currently provides a non-destructive readiness gate only; irreversible deletion, backup expiry, real cutover and production activation require owner approval. Daily scheduling/off-host storage examples are unactivated, not a configured production service. The pre-existing missing root .env.example still blocks release completeness.

## Hosting candidate

A single-origin Render staging configuration is prepared in deploy/render-build.sh and deploy/render-start.sh. It serves the React build, Django API and Admin together, with PostgreSQL17 and a separate private-media disk. No hosted deployment exists yet. See [deployment instructions](docs/DEPLOYMENT.md) for account, recurring-cost, release and database approval gates. Production learners and live AI remain disabled.


The reviewed staging candidate is published through the development branch with CI verification; publication does not activate hosted services. See [deployment and repository access](docs/DEPLOYMENT.md) for the separate Render permission and infrastructure gates.


A restricted free Render demonstration profile is prepared locally: same-origin React/Django/static delivery, private access, text-only synthetic content, disabled learner/AI features and no uploads. It preserves production security and uses verified external PostgreSQL TLS. It is not deployed. See [free-demo configuration](docs/DEPLOYMENT.md).

The restricted free-demo candidate is approved for main publication. GitHub visibility is Public with explicit owner approval. Render auto-deploy is Off; the start switch and manual deployment remain blocked on live profile/database prerequisites. See [deployment readiness](docs/DEPLOYMENT.md) and [current handoff](docs/AGENT_HANDOFF.md).
