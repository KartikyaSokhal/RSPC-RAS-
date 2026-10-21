# Phase A key-remediation verification — 21 October 2026

| Check | Actual fresh result |
|---|---|
| Frontend npm run check | **80 passed**, 10 files; ESLint/production build passed |
| Isolated backend suite | **121 passed/four PostgreSQL-only skipped** (125 discovered), 9.485s |
| Rotation checks | **9/9 passed**, 0.002s: distinct strong key, no fallback, old/new sessions, unchanged passwords/auth hashes, reset tokens, visitor cookies, both practice-token salts and quota HMACs |
| Django system/migration checks | No issues; makemigrations --check --dry-run reports no changes |
| Gitleaks v8.30.1 | Staged diff, full 223-file index export and reachable-history default-rule scans: exit 0, zero findings |
| Independent exact-value scan | No active environment/demo credential in index/history; one known retired historical key blob, zero remaining scoped active-workspace matches |
| Reuse/history | Five reachable commits/202 historical blobs inspected; two commits contain key; no other scoped active local reuse |
| Remote read-only assessment | SSH refs confirmed origin branch at ee272a6 and main at e6e7989 (containing retired key); gh unauthenticated, public API 404/visibility unknown |
| Preservation/release/Git/docs | 223 release inputs, exact index/worktree matching; 161 other protected hashes unchanged; only authorized ignored .env rotates; four SQLite integrity/FK checks clean; whitespace/fsck/document links pass |

Runtime: Node 24.22.0, Python 3.14.6, Django 6.0.9. Backend tests use isolated in-memory/disposable fixtures and mocked AI; host process visibility was permitted for the PDF guard. No original/demo database was migrated or changed. No fresh browser suite/clean-install/PostgreSQL service/remote CI/live-model/production verification is claimed. Prior cleanup's 28 Chromium/97 API/29 axe scans remain dated evidence only.

Private evidence: `../.recovery/prepal-key-remediation-ldmhun0a/`. Verified before.tar.gz protects the reviewed 223 inputs/.git/private environment; rotation.json confirms only SECRET_KEY changed. reuse-preflight.json, history-assessment.json, remote-heads.txt, expanded-known-value-scan.json, gitleaks-summary.json and redacted logs capture scope. rotation_checks.py/log, frontend.log/backend.log and final index/preservation/commit receipt provide actual execution. Tool binary/checksums stay in private tools/; no application dependency changed.

Reproduction: pinned-runtime npm run check; backend/run_tests.py with the backend interpreter and PYTHONDONTWRITEBYTECODE=1/PYTHON_DOTENV_DISABLED=1; backend/manage.py check and makemigrations --check --dry-run with core.test_settings; scripts/check_docs.py and --release; scripts/release_manifest.py; git diff --cached --check and git fsck --full --no-dangling. Gitleaks commands use git --pre-commit --staged; dir on an exact index export; git --log-opts='--all --full-history'; each uses --redact=100 --ignore-gitleaks-allow --report-format=json with private output. Default rules missed the known insecure-prefix development key, which independent exact matching caught; no additional risk was identified in the scanned scope. External credential reuse/visibility and unknown secrets cannot be ruled out by local scans.

The first final documentation scan classified a public commit SHA beside a key-related label in AGENT_HANDOFF as generic-api-key. Confirmed it was the Git revision, not a credential, and separated the revision list from that label. No scanner waiver/rule suppression was added; the final scans were rerun.

The owner authorized the named local commit if these conditions pass. No push, rewrite/amend, production credential access, paid API, cutover or deployment. Historic results below are not fresh verification.

---

# Controlled cleanup verification — 21 October 2026

Current evidence, superseding the historical results below. Branch `codex/prepal-1-0`, unchanged HEAD `ee272a6954868b303447545eb553200adb024a24`. Runtime: Node 24.22.0, Python 3.14.6, Django 6.0.9, local Chromium. Earlier uncommitted work remains preserved; no staging, commit, push, deployment or real PostgreSQL cutover occurred.

| Check | Actual local result |
|---|---|
| Original checkout frontend | **80 passed**, 10 files; ESLint and production build passed |
| Fresh release-copy frontend | **80 passed**, zero failed/skipped; ESLint and production build passed |
| Original checkout backend | 125 discovered: **121 passed, 4 PostgreSQL-only skipped**, zero failures |
| Fresh release-copy backend | 125 discovered: **121 passed, 4 PostgreSQL-only skipped**, zero failures, 11.654s |
| Django checks / migration consistency | No system-check issues; `makemigrations --check --dry-run` reports no changes in both environments |
| Fresh dependency installation | `npm ci --no-audit --no-fund` and hash-locked Python development requirements installed successfully in the disposable copy; `pip check` passed |
| Chromium fixtures | **15/15 passed**, 36.1s |
| Django/Admin/PDF/mock-Tutor integration | **9/9 passed**, 40.1s |
| Academic sample Chromium | **4/4 passed**, 43.8s |
| Sample API / practice | **97 query-only HTTP checks passed**; 15 lessons, 75 questions/300 choices, 19 tags, 30 approved links, five distinct 15-question subject pools |
| Automated accessibility | **29 axe scans, zero violations**; keyboard/mobile/theme coverage remains green |
| Recovery | Complete private archive: 26,913 file/symlink entries verified; independently restored original SQLite passes integrity/FK checks |
| Protected files | **162 hashes unchanged**, including all four existing SQLite databases, media, locks, models/migrations, dormant learner template and historical evidence |
| Git and packaging | `git diff --check`, `git fsck --full --no-dangling`, explicit 223-input manifest and local/release documentation-link checks passed; no staged changes |

The fresh environment is a hash-verified export of **current uncommitted worktree inputs**, not a clone of a published commit. Dependencies were installed only there; existing checkout dependencies and lockfiles were preserved. All browser suites ran serially against loopback servers; the Admin tests used a newly prepared synthetic demo, separate from the newly prepared academic sample. No existing demo was changed. Both disposable databases applied only the existing migration graph through 0008; no schema change or original-data migration occurred.

## Reproduction and evidence

Run from the application root with the pinned runtimes. Select NEW private demo destinations; never reuse valuable data for mutable integration tests.

```sh
npm ci
python3.14 -m venv backend/.venv
backend/.venv/bin/python -m pip install --require-hashes -r backend/requirements-dev.txt
npm run check
backend/.venv/bin/python backend/run_tests.py
PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/manage.py check --settings=core.test_settings
PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
backend/.venv/bin/python -m pip check
backend/.venv/bin/python scripts/check_docs.py
backend/.venv/bin/python scripts/check_docs.py --release
backend/.venv/bin/python scripts/release_manifest.py
git diff --check
git fsck --full --no-dangling
```

For browser reproduction, set PREPAL_DEMO_ROOT to a NEW private legacy-demo directory, run `scripts/prepare_demo.py` with the backend interpreter, then `PYTHON_DOTENV_DISABLED=1 npm run test:integration`. Select a DIFFERENT NEW private directory for `scripts/prepare_sample_demo.py --directory <new-directory>`; set PREPAL_DEMO_ROOT to that directory for `scripts/verify_sample_demo.py` and `PYTHON_DOTENV_DISABLED=1 npm run test:sample`. Run `npm run test:e2e` separately. Ensure the matching Playwright Chromium is installed as part of local setup; this batch reused the existing browser at `/private/tmp/prepal-p000-browsers`. Actual pinned Node runtime was `/private/tmp/prepal-p000-runtime/node-v24.22.0-darwin-arm64/bin`.

Private recovery/evidence is outside the checkout at `../.recovery/prepal-cleanup-20261021-d8aem1mu/`. It contains `VERIFIED.json`, `before.json`, modified/untracked/ignored inventories, `protected-data.json`, `cleanup-actions.json`, final file delta and release manifest, installation/check/browser logs and the disposable `release-copy/`. Browser evidence is in `browser-ui-results/`, `browser-integration-results/`, `browser-sample-results/`. Archive `Prepal-before.tar.gz` has SHA-256 `f304e12373cb2f245f6987405ef934743f375755c172765fa920cb310de97bfe`. Restore into a NEW private directory, never over the working tree. The recovery archive contains credentials and must remain private.

## Errors corrected and limits

- Full-syllabus/search UI showed invented fallback counts (including 152 topics). Counts now distinguish loading/error from a successful zero and derive only from the complete hierarchy. Three new tests cover unavailable, empty and filtered data.
- Canonical docs were ignored, and the first release-only link check exposed 31 links into excluded private archives. Ignore rules now admit canonical docs; private references are plain archival identifiers. Historical originals remain in the verified snapshot/private archive.
- The screenshot script embedded credentials and assumed a personal path/transitive package. It now loads private demo credentials, requires a loopback demo and uses the declared Playwright dependency. Lint passed; the screenshot script itself was **not executed**.
- Seven proven unused Python imports were removed. AST comparison against the snapshot confirms the six affected modules' executable bodies are otherwise unchanged. No historical log failure was treated as a current product defect.

All final checks above passed or have the explicit skips shown. There is no configured standalone TypeScript typecheck in this JavaScript application. PostgreSQL-specific tests were not run: no explicitly isolated disposable PostgreSQL target was supplied. Historical PostgreSQL results below are not fresh evidence. No vulnerability-advisory audit, live paid-provider call, production-load, physical-device or manual screen-reader verification was performed. Automated accessibility scans do not constitute certification.

Production blockers remain PostgreSQL roles/TLS/cutover and durable restore approval; domain/proxy/static/private-media configuration; independent content/rights review; live model/billing/cap validation; and a separately scoped PDF timeout mismatch (parser up to 60s, proxy 40s, Gunicorn 45s). Uploaded-PDF reading is verified; topic-note PDF export is not implemented. Phase 5 is not complete or started by this task.

---

# Historical verification records

The following dated sections preserve earlier decisions and evidence; their counts and limitations describe their respective batches, not the current cleanup run.

# Academic sample verification — 21 October 2026

Story: the existing syllabus opens published sample notes, contextual links and tag pages through the unchanged API; canonical subject collections return and grade the 75 stored sample questions without saved learner state. Runtime: existing Python 3.14.6/Django 6.0.9, pinned Node 24.22.0 and local Chromium. No dependencies installed or application/provider implementations changed.

| Check | Actual result |
|---|---|
| Corpus/seed | 142 original topic IDs/titles/slugs/parents; five roots; 15 leaf lessons, 6,754 note words (428–480 each); 75 MCQs/300 options |
| Published discovery | 30 publications (15 lessons + 15 ancestors), 19 controlled tags, 15 aliases, 30 approved edges and 30 active approved links; zero pending proposals |
| API under SQLite query-only | 97 requests checked; 15 detail/context/legacy quiz routes, repeated stable quiz IDs, all tag pages, five pools and CSRF-protected perfect grading, contained learner routes and empty draft placeholders |
| Backend | 125 discovered: **121 passed, 0 failed, 4 PostgreSQL-only skipped**, 9.485s; includes five new corpus/refusal/fresh-demo tests |
| Frontend | **77 passed, 0 failed/skipped**, nine files |
| ESLint / production build | Both exit 0; new sample suite/config included in lint |
| New real-Django sample Chromium | **4 passed, 0 failed/skipped**, 43.8s: all 15 notes/popups, 19 tag pages, five subject pools and all 75 correct answers, mobile focus/new-tab/themes |
| Existing Chromium fixture suite | **15 passed, 0 failed/skipped**, 36.1s |
| Existing Django/mock integration | **9 passed, 0 failed/skipped**, 39.9s, including Admin publication/withdrawal, connection decisions, PDFs, search, mock Tutor and stateless quiz |
| Automated accessibility | 29 scans, zero violations: ten existing UI, 17 existing integration, two sample mobile light/dark; sample screenshots inspected |
| Data integrity | Original SQLite, both older demos and new sample: integrity ok and zero foreign-key errors; all 25 baseline data/config/migration files unchanged |
| Documentation / whitespace | 34 active document link targets valid; git diff --check passed |

## Reproduction

Run commands from the application root with the supported Node version. Tests never use the original SQLite or a production database.

```sh
backend/.venv/bin/python backend/run_tests.py
npm run test
npm run lint
npm run build
PREPAL_DEMO_ROOT="$PWD/.local/sample-content-v1" backend/.venv/bin/python scripts/verify_sample_demo.py
PREPAL_DEMO_ROOT="$PWD/.local/sample-content-v1" PYTHON_DOTENV_DISABLED=1 npm run test:sample
npm run test:e2e
# Existing integration corpus is deliberately separate from the new academic samples.
PREPAL_DEMO_ROOT=/private/tmp/prepal-sample-legacy-test PYTHON_DOTENV_DISABLED=1 npm run test:integration
backend/.venv/bin/python scripts/check_docs.py
git diff --check
```

The legacy integration directory was freshly created for this run using `scripts/prepare_demo.py`; preserve it if it already exists. For a future clean regression run select a different new private directory and prepare its legacy fixtures first. Both preparation scripts refuse existing databases; the sample preparation script refuses the entire existing destination. Browser suites run serially because they rebuild shared dist. Pinned runtime PATH was `/private/tmp/prepal-p000-runtime/node-v24.22.0-darwin-arm64/bin`; PLAYWRIGHT_BROWSERS_PATH was `/private/tmp/prepal-p000-browsers`.

New seed/read-only verifier tests assert repeated preparation and direct reseeding fail without changing database bytes; symlink aliases and existing sentinel files are preserved. `create_sample_content` refuses normal test/application settings before ORM access. All 75 questions have four distinct choices, one correct answer, explanations and the intended primary leaf. Subject membership follows ancestry; subject pools are disjoint, 15 questions each. Each lesson has three tags; links use normal evidence-bound approval and sanitized snapshots, with no stored HTML rewrite.

## Actual failures and corrections

The first targeted/API run incorrectly expected HTTP 404 for an unselected syllabus topic. Existing behavior intentionally returns a 200 coming-soon placeholder with empty blocks. The verifier was corrected to assert that contract and the context endpoint's 404; application behavior was unchanged. The final five new tests pass in the full backend run.

The first full backend sandbox run had one PDF regression failure because `/bin/ps` was denied by the sandbox, preventing the existing parser memory guard from operating. The host-permitted isolated run passed all 121 applicable tests without application changes. Initial sample browser startup likewise could not bind loopback inside the sandbox; the permitted host run passed. One existing-browser automatic permission review timed out before execution; its single permitted retry succeeded. No check remained blocked by approval review.

## Evidence and limitations

Private evidence root: `/var/folders/xm/np82ybsx4vd25hkyxxr131200000gn/T/prepal-sample-content-mkpgvnqp`. `before.json`/`git-before.txt` capture the starting dirty worktree; final manifests record this task's exact changes and source hashes. Seed/API/backend/frontend/lint/build/Chromium logs and selected screenshots are retained there. Browser output directories are `/private/tmp/prepal-sample-browser-results`, `/private/tmp/prepal-sample-existing-browser` and `/private/tmp/prepal-sample-legacy-browser`. Credentials and databases stay in private ignored directories.

Original SQLite remains content migration 0004, SHA-256 `3c3252fef33ff6cec64e2c5a0eb52842ebf69abb14099c809db9298e2bab9387`. Existing demos are unchanged at 152 and 10 topics. New sample and disposable regression databases alone received the existing migration graph through 0008. No migration files, models, real PostgreSQL target or cutover changed. PostgreSQL-specific tests were not run in this SQLite sample task.

Source checks support local sample quality, not independent human academic approval or official examination coverage. Browser tests block external origins and validate reference hrefs, not continued external-site availability. No physical device, manual screen-reader, production load or live paid-model validation occurred. The sample has no new PDFs; existing PDF functionality passed on synthetic legacy fixtures. Prior UI copy such as generic “Verified study notes” remains unchanged; the demo banner and each lesson's explicit non-production notice qualify sample status. Phase 5 remains unstarted and separately gated.

---

# Phase 4B verification — 20 October 2026

Frontend-only implementation. Private evidence root `/private/tmp/prepal-phase4b-_8unf9dv`; `ui-docs-before.tar.gz` and `before.json` protect previous work. No dependencies installed, backend files changed or migration commands run. Existing Phase 3 results below are historical and were not promoted to fresh backend/PostgreSQL evidence.

| Check | Actual result | Evidence |
|---|---|---|
| Frontend Vitest | 77 passed / 0 failed / 0 skipped, nine files | `frontend-final.log` |
| ESLint | Exit 0, no errors | `lint-final.log` |
| Vite production build | Exit 0 | `build-final.log`; browser webservers also built successfully |
| Full Chromium fixture suite | 15 passed / 0 failed / 0 skipped, 37.8s | `chromium-fixtures-acceptance.log`, `browser-fixtures-acceptance/` |
| Selected Django/mock student journeys | 7 passed / 0 failed / 0 skipped, 43.0s | `chromium-integration.log`, `browser-integration/`; two Admin tests not selected |
| Automated accessibility | 27 scans, zero violations | Ten new fixture scans; 14 existing principal-page/theme plus two popup and one tag scan in integration |
| Source integrity/preservation | SQLite integrity ok/FK errors zero; original source/demo/.env/migrations/backend/history hashes unchanged | `preservation.json`; final changed-file manifest |
| Documentation/whitespace | Local links in 34 active documents and `git diff --check` passed | `docs-check.log`, `diff-check.log` |

## Actual commands

Pinned runtime: `/private/tmp/prepal-p000-runtime/node-v24.22.0-darwin-arm64/bin`; existing packages only. Browser path `/private/tmp/prepal-p000-browsers`. Keep browser suites serial because they rebuild shared dist. Test servers bind only 127.0.0.1 (4173 or 4175/8001), and are stopped by Playwright afterward.

```sh
npm run test
npm run lint
npm run build
npm run test:e2e -- --output=/private/tmp/prepal-phase4b-_8unf9dv/browser-fixtures-acceptance
PREPAL_DEMO_ROOT=/private/tmp/prepal-phase4b-_8unf9dv/integration-demo PYTHON_DOTENV_DISABLED=1 \
  npm run test:integration -- e2e-integration/journey.spec.js e2e-integration/discovery.spec.js \
  --grep-invert 'Admin Suggest' --output=/private/tmp/prepal-phase4b-_8unf9dv/browser-integration
backend/.venv/bin/python scripts/check_docs.py
git diff --check
```

The integration destination was copied from the previously verified `/private/tmp/prepal-phase3-fj72pzoi/browser-demo-final-acceptance`, which already has schema 0008. No migration or demo-preparation command was invoked. Only the new disposable copy received mock Tutor usage writes. Do not reuse `.local/demo`, source data or a valuable application database. Demo settings disable `.env` loading, force `AI_MODEL=mock-demo-no-network` and an empty provider key. Fixture requests are intercepted and external origins blocked. Chromium initially could not bind a loopback port inside the sandbox (EPERM); the authorized checks then ran with host loopback access. No automatic approval rejection occurred.

## Acceptance covered

- One prominent existing `/search` entry and working light/dark toggle; no header auth/Syllabus/About links. Existing routes and footer syllabus/help remain.
- Dynamic root/all-descendant counts share one hierarchy response, with loading/error states and a shared retry. Synthetic five-root fixture has 14 nodes; source has five roots/142 nodes; the old Admin-mutated integration fixture has six roots, intentionally not sliced to five.
- API subject buttons scroll/focus their original root. Expand All opens every node; Collapse All hides descendants while five fixture root labels remain; click/Enter/Space individual toggles still work. Filtered tree positions retain 1/1.2/B/A/5/5.1 rather than renumbering filtered siblings. Deeper letters restart per parent.
- Original SVG aspect ratio remains 600:560; tested widths 320, 390, 768, 1024 and 1280, wrapping controls, visible focus and bounded header/tree/Tutor. One nonmodal launcher; Escape/Close restore focus without scrolling, and the composer stays in view. Stable screenshots were visually inspected after finite entrance animations.
- Existing Phase 3 security regressions, current published context/new-tab/focus/scroll, approved links, tags/related topics, collection grading and no learner activation remain covered. Real Django/mock journeys retain selected passages, citations, PDF rendering, search and stateless answer retry.

## Initial failures corrected and limits

New unit checks initially used textbox for a search input, assumed jsdom role queries hide closed-details descendants, and queried the lazy shell before it mounted. Selectors now use searchbox, actual visibility and awaited landmarks; application behavior was not relaxed. First Chromium scans measured color/background transitions immediately after theme selection. Removed unnecessary tree text-color animation and await finite theme/entrance motion before static contrast scans/screenshots; both static themes pass. This is automated steady-state coverage, not accessibility certification.

No backend unit suites, Admin workflows, PostgreSQL tests, migration/reversal/cutover or dependency/network audits were rerun in this frontend-only phase. Existing backend/migration specs and all historical evidence remain unchanged. Browser viewport emulation is not physical-device, virtual-keyboard or manual screen-reader evidence. Large-corpus performance and prior Phase 3 publication/scan bounds remain. Current exact next task: obtain owner’s Phase 5 brief/acceptance criteria/approval; stop before implementation.

---

# Historical Phase 3 verification — 20 October 2026

Actual branch `codex/prepal-1-0`, unchanged HEAD `ee272a6954868b303447545eb553200adb024a24`. Existing uncommitted changes are preserved. Tests use Python 3.14.6, Node 24.22.0, PostgreSQL 17.11 and psycopg 3.3.6. No dependencies were installed, real AI requested or real data migrated.

| Check | Actual Phase 3 result |
|---|---|
| Full PostgreSQL backend | 120/120 passed on fresh test DB, real migration graph |
| Full SQLite backend | 120 discovered: 116 passed, four PostgreSQL-only skips |
| New discovery coverage | 18 feature/API/security/query-bound tests plus PostgreSQL and SQLite migration roundtrips |
| Frontend | 68/68 across eight files; lint and production build passed |
| Chromium fixture | 9/9 passed, including active-markup rejection and learner containment |
| Django/mock Chromium | 9/9 passed: existing five plus desktop/mobile popups, tag/subject practice and Admin Suggest/approve/reject |
| Accessibility | Existing 14 page/theme scans plus two popup viewports and one tag page: 17 scans, zero automated violations; not certification |
| Original SQLite / existing demo / .env | Hashes unchanged from preflight; original content remains 0004, integrity ok, FK errors zero |
| Source backup/copy | Verified backup/restore; actual 0005–0008 migrations preserve all 437 original rows/columns/PKs and high-water counters |
| Source-data PostgreSQL transfer | 34 tables / 518 migrated rows / 32 sequences matched; six rolled-back smoke workflows passed |
| Populated synthetic transfer | 34 tables / 193 rows; approved proposal/reviewer/occurrence/plan JSON, tag flags, M2M IDs, deleted counters and one media file preserved |
| Reversal / reapplication | PostgreSQL and SQLite 0007 → 0008 → 0007 → 0008 preserve old tag/association IDs; SQLite deleted Tag counter 9002 retained; no automatic tag/proposal approval |
| Drift / docs / quota | No migration drift; 34 active Markdown files' local links passed; SQLite eight-contender quota race retained 4000-micro ceiling |

## Actual commands and environment

Use the existing virtualenv and pinned Node; no real .env is loaded by tests. macOS host process visibility is needed for bounded PDF parser monitoring. PostgreSQL used an isolated tmpfs Docker container, loopback 55434, generated private credentials, base `prepal_test_phase3` and fresh `test_prepal_phase3`. The test runner refuses existing test databases/nonlocal targets. Container is stopped after verification.

```sh
backend/.venv/bin/python backend/run_tests.py
# Explicit local POSTGRES_* plus PREPAL_TEST_POSTGRES=1; no backend/.env.
backend/.venv/bin/python backend/run_tests.py --postgres
backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
backend/.venv/bin/python scripts/verify_postgres_transfer.py
backend/.venv/bin/python scripts/rehearse_postgres.py \
  --sqlite-source "$PWD/backend/db.sqlite3" \
  --source-media "$PWD/backend/private-media" \
  --new-directory /absolute/private/NEW-rehearsal
npm run check
npm run test:e2e -- --output=/absolute/private/new-fixture-results
# Prepare a NEW private synthetic demo and use the SAME PREPAL_DEMO_ROOT.
PREPAL_DEMO_ROOT=/absolute/private/NEW-demo backend/.venv/bin/python scripts/prepare_demo.py
PREPAL_DEMO_ROOT=/absolute/private/NEW-demo npm run test:integration -- --output=/absolute/private/new-integration-results
backend/.venv/bin/python scripts/verify_budget_race.py
backend/.venv/bin/python scripts/check_docs.py
git diff --check
```

Run browser suites serially because they rebuild shared dist. Actual Chromium runtime was `PLAYWRIGHT_BROWSERS_PATH=/private/tmp/prepal-p000-browsers`; final integration root was `/private/tmp/prepal-phase3-fj72pzoi/browser-demo-final-acceptance`. Use new destinations on repeats, never the existing .local/demo.

Private evidence root `/private/tmp/prepal-phase3-fj72pzoi`: pre-change worktree archive/hash manifest, source backup, `sqlite-final.log`, `postgres-final.log`, `frontend-acceptance.log`, `chromium-fixture-final.log`, `chromium-integration-final-acceptance.log`, `synthetic-transfer-verified.log`, `source-rehearsal-verified/result.json`, final preservation/file manifest and desktop/mobile popup screenshots under browser-integration-final-acceptance. Private copies/credentials/records must not be published. Source hash: `3c3252fef33ff6cec64e2c5a0eb52842ebf69abb14099c809db9298e2bab9387`.

## Verified behavior and failures corrected

Meaningful whole phrases use Unicode NFKC/casefold/whitespace with original UTF-16 offsets. Whole-word boundaries include combining marks. Longest overlapping approved spans win before duplicate-target suppression; total eight across blocks, no self-links. The initial overlap test exposed shorter fallback links inside repeated longer phrases; resolving all overlaps first fixed it. A Unicode helper test was corrected to use the normalized vocabulary contract. An initial overlong index name was shortened before accepting system checks.

Only approved current source-bound proposals activate links. Re-analysis retains approval/rejection; edited HTML requires fresh evidence approval. Draft/withdrawn/ambiguous targets and revoked aliases/proposals fail closed. Bounded, query-tested reader GETs do not call matching or plan construction and issue no inserts/updates/deletes. Live popup context checks suppress a newly withdrawn target even from an older reader page. No stored article HTML is rewritten.

Initial popup unit tests found focus was lost when React rewrote identical innerHTML during popup state changes. Memoizing the sanitized HTML property preserves trigger DOM/focus; real keyboard/mobile/new-tab tests passed. An empty-tag test initially matched the loading status; it now waits for the actual empty state. Admin browser tests originally used a nonexistent “Go” label; Django 6 uses “Run”. The synthetic fixture also received an explicit cross-topic phrase so suggestion review has real evidence. No application validation was bypassed to pass these tests.

The Admin action tests verify Suggest Connections, phrase/target/context review, reject/approve permissions and recorded decisions. Queue tests verify prioritized source scans, fair bounded draining and new-title/new-alias rechecks. Tag tests cover default privacy, released associations, stable URLs, unknown/empty/withdrawn results. Collection tests cover child/related aggregation, current review/visibility, 50+1 pagination with no duplicate IDs, membership/choice/token/CSRF/malformed errors and repeatable grading with zero attempts/questions/quizzes written.

## Remaining limits

Matching intentionally stays within one text node and skips existing anchors/headings/code; cross-formatting phrases require editorial adjustment/manual safe links. Ambiguous terms are withheld. Each editorial workflow processes a bounded batch (20 by default); drain the remainder with regenerate_connections. Unavailable cached spans are removed on reads without expensive fallback matching; regenerate to fill unused slots. Open tabs are not polled. General related syllabus links are independent of rejected phrase proposals.

Public tag/collection pages paginate, and collection validation fingerprints full matching quizzes; large-corpus load testing remains pending. Publication resolution retains the existing 5000-entry bound. Only one prior publication is retained. Reversing 0008 removes Phase 3 metadata, so back it up before an approved rollback. Source data is not editorially reviewed by fixture tests.

Remote CI, paid Gemini, real PostgreSQL cutover, production TLS/roles/media/durable recovery/load and physical devices remain unverified. No paid service, learner activation, commit, push or deployment occurred. Exact next task: obtain Phase 4 scope/acceptance criteria and approval; do not implement Phase 4.

---

# Historical Phase 2 verification — 20 October 2026

Branch `codex/prepal-1-0`, unchanged HEAD `ee272a6954868b303447545eb553200adb024a24`. Verification uses pinned Python 3.14.6/Node 24.22.0, psycopg 3.3.6 and loopback PostgreSQL 17.11. No dependency installation or production connection was needed. Real AI clients and sockets are forbidden in backend tests; browser demos use the mock provider and cleared keys.

| Verification | Actual Phase 2 result |
|---|---|
| Django / disposable PostgreSQL | 100/100 passed, actual migration graph, Admin/API/PDF/security/quota regressions |
| Django / SQLite :memory: | 100 discovered: 97 passed, three PostgreSQL-only tests skipped |
| New foundation coverage | 13 content/Admin/registry/MCQ tests, one PostgreSQL migration roundtrip and one separate SQLite migration roundtrip |
| PostgreSQL reversible migration | 0006 → 0007 → 0006 → 0007 repeatedly; legacy questions/choices/review hashes, learner rows/through IDs preserved |
| SQLite reversible migration | New synthetic file; forward/reverse/reapply retained original fields/PKs and deleted Topic/Question counters 9000/9001 |
| Frontend | 59/59 in seven files; lint and production build passed |
| Chromium fixture tests | 9/9 passed; safe reading/chat rendering and learner containment |
| Real Django/mock Chromium integration | 5/5 passed; full Admin create/edit-form/preview/review/publish/withdraw plus existing four student journeys |
| Accessibility | Existing 14 student-page/theme scans reported zero automated violations; not certification |
| Source migration/backup/restore | Source read-only; copy genuinely applied 0005–0007; 437 old rows/IDs/high-water counters preserved |
| Source-data PostgreSQL transfer | 32 tables / 507 post-migration rows / 30 sequences matched; six rolled-back smoke checks passed |
| Populated synthetic PostgreSQL transfer | 32 tables / 177 rows; six new registry/M2M tables populated; explicit IDs and deleted-ID counters preserved; one media file verified |
| Original real/demo databases | Byte-identical to preflight; source integrity ok, zero FK violations; original content migration remains 0004 |
| Drift/docs/quota | No migration changes detected; 34 active Markdown files' local links passed; eight-contender SQLite quota race respected 4000-micro cap |

## Commands and private evidence

Run from the application root, with Node selected by `.nvmrc` and existing `backend/.venv`. Full command guidance below remains valid. Final commands included:

```sh
backend/.venv/bin/python backend/run_tests.py
# Explicit generated local POSTGRES_* environment, PREPAL_TEST_POSTGRES=1;
# base prepal_test_phase2, fresh test_prepal_phase2, loopback port 55433.
backend/.venv/bin/python backend/run_tests.py --postgres
backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
backend/.venv/bin/python scripts/verify_postgres_transfer.py
backend/.venv/bin/python scripts/rehearse_postgres.py \
  --sqlite-source "$PWD/backend/db.sqlite3" \
  --source-media "$PWD/backend/private-media" \
  --new-directory /private/tmp/prepal-phase2-nj3tf0nd/source-rehearsal-final
npm run check
npm run test:e2e -- --output=/private/tmp/prepal-phase2-nj3tf0nd/browser-fixture-results
# Fresh synthetic demo first, with the SAME PREPAL_DEMO_ROOT in both commands.
PREPAL_DEMO_ROOT=/absolute/private/NEW-demo backend/.venv/bin/python scripts/prepare_demo.py
PREPAL_DEMO_ROOT=/absolute/private/NEW-demo npm run test:integration -- --output=/absolute/private/new-results
backend/.venv/bin/python scripts/verify_budget_race.py
backend/.venv/bin/python scripts/check_docs.py
git diff --check
```

The already-created rehearsal/demo directories above are evidence, not reusable destinations; select new paths when repeating. Actual successful integration used `PREPAL_DEMO_ROOT=/private/tmp/prepal-phase2-nj3tf0nd/browser-demo-final-acceptance`. Chromium runtime: `PLAYWRIGHT_BROWSERS_PATH=/private/tmp/prepal-p000-browsers`. Run fixture and integration suites serially because both rebuild the shared dist directory; use distinct output directories. Host process visibility is required for macOS PDF memory monitoring.

Private root `/private/tmp/prepal-phase2-nj3tf0nd` contains the pre-change 337-file archive/hash manifest, source backup, final changed-file manifest, `backend-sqlite-final.log`, `postgres-tests-final.log`, `frontend-verified.log`, `chromium-fixture-final.log`, `chromium-integration-final-acceptance.log`, `transfer-synthetic-final.log` and `source-rehearsal-final/result.json`. These may contain private data/temporary credentials; do not publish the directory. No secrets are included in this report. Source hash is `3c3252fef33ff6cec64e2c5a0eb52842ebf69abb14099c809db9298e2bab9387`.

## Failures investigated and corrected

- Initial backend assertions expected old navigation and implicit relation approval; updated fixtures now explicitly approve synthetic educational edges. Sandbox-only PDF parsing failed because `/bin/ps` was denied; host-visible isolated runs passed.
- SQLite's model-only runner left cached ContentType IDs pointing to rolled-back test rows. New tests clear that manager cache before fixtures; final SQLite/PostgreSQL suites pass.
- Concurrent browser suites interfered through shared dist/output files, causing missing assets/traces and fixture failures. Serial execution with separate output folders passed.
- New Admin browser selectors initially matched multiple links, assumed a hand-entered slug while Django prepopulation was active, and required a success CSS class for an informational message. Selectors now use the result table, saved slug and Django message list. These were test-harness corrections.
- A genuine WYSIWYG bug submitted untouched `<p><br></p>` extra inlines as new incomplete blocks. Empty editor values now remain empty on blur/source/submission. The full-form browser workflow passed after the fix; no validation was disabled.
- Migration review identified SQLite table rebuilds can lose deleted-ID high-water marks. 0007 field operations preserve them in both directions; a real migration roundtrip proves it on a new synthetic file.

## Compatibility and limits

Standalone ContentBlock saves no longer publish automatically; editors must explicitly review/publish the topic. New relationships start draft and require approval. Matching already-reviewed stored edges preserve approval; revoking an edge suppresses it from resolved published snapshots. Tag assignments freeze on publication/restore, with the primary syllabus location still the existing Topic FK. Aliases remain unused by public search/links/Tutor until Phase 3.

New/moved MCQ Admin associations require leaf subtopics and cannot repeat the primary as related. Legacy ancestor-level locations remain editable and unchanged. Existing default backfills retain quiz review fingerprints; changed classification/tags require re-review. Question collections do not copy rows or implement arbitrary cross-quiz assembly. Rich-text allowlists, supported resources and one-previous-snapshot retention remain unchanged. Unsafe SVG/iframe/scripts/handlers/styles remain unsupported; no stored real content was rewritten.

No real cutover, original migration, paid AI request, public deployment, commit, push or remote CI occurred. Production TLS/roles/load/durable backup recovery, physical devices, real corpus rights/factual review and live Gemini remain unverified. Exact next task is **Phase 3 dynamic content linking and discovery**, awaiting separate approval.

---

# Phase 1 reproducible verification

Tests use synthetic fixtures, mocked providers and isolated databases. `backend/run_tests.py` never loads the real .env and now discovers tests correctly from either repository root or backend. SQLite uses :memory: with model-created tables; PostgreSQL uses actual migrations in a fresh local test database. Existing real and demo databases are excluded. Browser integration refuses a missing PREPAL_DEMO_ROOT or the original .local/demo path before starting servers; use an absolute separate synthetic directory.

```sh
npm run check
backend/.venv/bin/python backend/run_tests.py
backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
backend/.venv/bin/python scripts/verify_budget_race.py
# Explicit local POSTGRES_* plus PREPAL_TEST_POSTGRES=1;
# base DB prepal_test_*; target test_prepal_* must not exist.
backend/.venv/bin/python backend/run_tests.py --postgres
backend/.venv/bin/python scripts/verify_postgres_transfer.py
npm run test:e2e
# Use a NEW private demo directory; preparation refuses an existing database.
PREPAL_DEMO_ROOT=/absolute/private/new-browser-demo backend/.venv/bin/python scripts/prepare_demo.py
PREPAL_DEMO_ROOT=/absolute/private/new-browser-demo npm run test:integration
backend/.venv/bin/python scripts/check_docs.py
```

| Verification | Actual Phase 1 result |
|---|---|
| Baseline backend | 76/76 on isolated host run; initial sandbox PDF monitor failure documented |
| Baseline frontend | 59 tests, lint and build passed |
| Final backend SQLite | 85 discovered; 83 passed, 2 PostgreSQL-only concurrency tests skipped |
| Final backend PostgreSQL | 85/85 passed; real migrations and fresh test DB create/destroy |
| Frontend | 59/59; lint/build passed, including pinned Node 24.22.0 verification |
| Chromium fixture suite | 9/9 passed; API fixtures, learner URL containment, rendering security |
| Real Django/browser integration | 4/4 passed on separate synthetic demo; desktop/mobile, tutor/PDF/practice, CSP |
| Accessibility | 14 page/theme scans passed with zero reported automated WCAG violations; not certification |
| Source copy migrations | 0005/0006 applied on copy; 437 original rows/IDs/counters preserved |
| PostgreSQL transfer | 26 tables/496 rows/24 sequences matched; all original data retained |
| Synthetic all-type transfer | 26 tables/160 rows, explicit M2M/framework IDs, Unicode/JSON, file reference, deleted-ID counters preserved |
| Native PostgreSQL restore | 26 tables and 24 sequences matched in an independent fresh DB |
| Browser configuration safety | Four integration tests discover with the explicit private demo; missing/default demo settings rejected before server startup |
| Migration drift | No changes detected; no model/migration file modification |
| SQLite quota race | Eight contenders, 4,000-micro cap enforced, over-cap request denied |

Pinned runtime files recommend Node 24.22.0 and Python 3.14.6. Initial local frontend/fixture-browser checks also passed with installed Node 26.5.0. PostgreSQL server 17.11 and psycopg 3.3.6 were used. macOS host process visibility was necessary for bounded PDF subprocess monitoring; sandbox-only PDF failure is not a product pass.

The first integration run had three timeouts caused by obsolete homepage CTA selectors; existing UI was not rebuilt. Corrected selectors/theme/popup assertions passed all four tests. PostgreSQL first exposed an old test's explicit streaming-response close ending the test transaction connection; consuming the test stream fixed it. Synthetic fixture harness path/PK syntax failures were corrected before accepting its transfer proof. Exact commands, protected files and limitations are in evidence (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).

GitHub Actions now includes a disposable PostgreSQL service, full database regressions and synthetic transfer. Remote CI was not triggered or verified. Live Gemini, production TLS/host/load/backup retention, real corpus approval and physical-device checks were not executed.
