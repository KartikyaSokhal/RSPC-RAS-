# Current AI handoff — remediated Phase A local release

Branch **codex/prepal-1-0**, origin `git@github.com:KartikyaSokhal/RSPC-RAS-.git`. Verification/base commit **ee272a6954868b303447545eb553200adb024a24**. The owner authorized the local commit **Prepare Prepal content-first MVP release baseline** once security conditions pass. The release is the commit containing this updated handoff; resolve the exact SHA with `git log -1 --format=%H -- docs/AGENT_HANDOFF.md` (the execution receipt/final response records it explicitly). No self-referential SHA is embedded in its own commit. Read AGENTS, current status/security/testing and the owner's next brief. No push, history rewrite/amend, deployment, live AI, production secret access or real cutover is authorized.

## Remediation and files changed

Confirmed the exposed historical key was loaded by development backend/.env (DEBUG true, production mode unset). A scoped workspace text scan found only that file; no matching inherited key or running application server. Rotated only SECRET_KEY atomically using 64 random bytes, mode 0600, with no old-key fallback; Django now loads the replacement. Other environment fields/passwords/data are unchanged. The ignored .env is NOT a release input. Independent demo/test keys remain unchanged.

Affected historical commits:

- `e6e7989db8c24eee59f8c38600cd619939c96856`
- `84186c913572ca3edde66572b8f2f2c8409ba6eb`

Read-only SSH confirmed GitHub main at e6e7989 and branch at ee272a6 before local commit. Treat the old value as disclosed; it is retired locally and rejected by the current production insecure-prefix guard. No history rewrite is needed for local retirement or authorized here. External reuse is unknown; never reuse historical/development/demo/test keys in production. gh CLI lacks login and unauthenticated API 404 does not establish visibility. SSH reading works; no remote ref changed.

Remediation edits only ignored backend/.env and existing documentation: AGENTS.md, README.md, backend/README.md; docs MVP_SCOPE, IMPLEMENTATION_PLAN, TASKS, DECISIONS, DEPLOYMENT, FEATURES, SECURITY, CHANGELOG, PROJECT_STATUS, TESTING, AGENT_HANDOFF. Existing application/models/migrations/locks remain exactly as the reviewed candidate. The baseline has all **223 release inputs**, **145 changed paths** versus base HEAD (74 added/69 modified/two approved starter SVG deletions). Exact full staged list is retained in the previous Phase A review and refreshed private final evidence. No private database/.env/media/backup/dependencies/generated output/history enters Git.

## Impact, verification and data

Old local authenticated sessions/session signatures, password-reset links, visitor cookies and signed practice tokens intentionally stop validating; users reauthenticate/reload. Development visitor/quota HMAC identities change. No session rows, password hashes, learner/content records, quota history or media are deleted/rewritten. Nine in-memory checks verify old rejection/new validity and password preservation. Four source/demo databases remain hash-identical with integrity ok/FK0. Of the prior 162 protected files, only the authorized backend/.env changes; the other 161 remain unchanged. Original SQLite stays content 0004, existing demos 0008/0005/0008; no new migration or schema/model change. Learner features stay disabled.

Fresh checks: **80 frontend passed**, lint/build passed; **121 backend passed/four PostgreSQL skips**, **nine rotation checks passed**, Django/migration/docs/Git checks clean. Checksum-verified Gitleaks v8.30.1 reports zero findings for staged diff/full index/history. Independent exact-value scans found no exposed current environment/demo secret and only the retired historical blob. Five reachable commits/202 blobs were assessed before commit. No additional high-risk issue was found within scope; scanning is not exhaustive. No fresh Chromium/clean-install/remote CI/PostgreSQL/production validation is claimed; previous cleanup evidence below is historical.

## Recovery and exact next task

Private evidence/checkpoint: `../.recovery/prepal-key-remediation-ldmhun0a/` (before.tar.gz, rotation.json, reuse/history/remote/scanner reports, nine-check script/log, frontend/backend logs, final release manifest/index review, COMMIT_RECEIPT.json). The retired value/private environment exist only in protected recovery and inactive history, never printed; backups must not reactivate it. Prior full recovery and Phase A checkpoints remain intact. Restore only to a NEW private directory, not over this tree.

**Exact next task: obtain separate Phase B push approval.** Once approved, reverify the release commit/remote, push this branch without rewriting history, compare remote SHA and check CI using approved GitHub access. Do not infer push approval from the local commit. Stop after local verification/commit now. Phase C topic-note PDF export/strict current-topic Tutor is not implemented; existing retrieval can opt into related topics. Subsequent approved PostgreSQL source/roles/TLS/durable encrypted backup/cutover, provider/domain, timeout alignment, staging acceptance and production release gates remain. No production URL exists.

The handoff below records historical cleanup implementation, not current authority.

---

# AI handoff — controlled cleanup complete locally

21 October 2026. Application Git root: `Prepal/`; origin `git@github.com:KartikyaSokhal/RSPC-RAS-.git`. Branch **codex/prepal-1-0**; unchanged HEAD **ee272a6954868b303447545eb553200adb024a24**. Read AGENTS, PROJECT_STATUS, TESTING and the owner's next brief first. All prior Phase 1–4B/Admin/editor/sample work remains dirty and preserved. No stage, reset, clean, commit, push, deployment or real PostgreSQL cutover is authorized by the cleanup task. Phase 5 remains unstarted.

## Recovery and preserved state

Private recovery is OUTSIDE the application checkout: `../.recovery/prepal-cleanup-20261021-d8aem1mu/`. `Prepal-before.tar.gz` includes the pre-cleanup .git and modified/untracked/ignored files. Verified 26,913 files/symlinks, 7,878 directories; compressed 146,326,806 bytes; SHA-256 `f304e12373cb2f245f6987405ef934743f375755c172765fa920cb310de97bfe`. All archive entries matched the source manifest and the source was stable during snapshot. Independent original SQLite restore passed integrity/FK checks. Restore only to a NEW private directory; never extract over this working tree. Recovery includes credentials and must not enter Git.

`before.json`, `modified.json`, `untracked.json`, `ignored.json`, `git-status-before.txt`, `VERIFIED.json`, `cleanup-actions.json`, `protected-data.json`, final delta and release manifest retain exact inventories/results. All **162 protected file hashes** remain unchanged: original/demo data and media, locks, models/migrations, historical evidence and dormant learner template. The parent `.git_inactive_backup` was not touched. No valuable data was deduplicated or deleted.

## Cleanup implementation files

| Files | Change |
|---|---|
| `.gitignore` | Hide private/generated output; allow canonical docs and shared IDE settings |
| `.vscode/settings.json`, `prepal.code-workspace` (new) | Application-only workspace and files/search/watcher exclusions; keep active dependencies |
| `src/pages/syllabusPage.jsx`, `src/pages/searchPage.jsx` | Remove invented fallback counts; handle loading/error/empty honestly; derive hierarchy depth/counts |
| `src/test/counts.test.jsx` (new) | Three regressions for unavailable, empty and filtered hierarchy counts |
| `backend/content/admin.py`, `views.py`, `services/connections.py`, `services/discovery.py`, `services/practice.py`, `services/pdf_extract.py` | Remove seven unused imports; executable-body AST equivalence verified |
| `backend/gunicorn.conf.py` | Correct database wording in docstring only; runtime timeouts unchanged |
| `scripts/capture_admin_screenshots.mjs` | Private credential file, explicit demo root, loopback/demo validation, declared Playwright dependency and current Admin captures |
| `scripts/release_manifest.py` (new), `scripts/check_docs.py` | Explicit hashed release inputs, private-value checks/export; release-aware Markdown target validation |
| `.github/workflows/checks.yml` | Add release-manifest/docs and fresh-sample verification/browser checks; remote CI not run |

Removed: `public/vite.svg`, `src/assets/react.svg` (zero source references), four Finder metadata files, seven generated Python cache directories and stale `dist/`. Build/test execution may regenerate ignored caches/dist. No dependencies were deleted for appearance.

Archived, hash/target verified: `backend/src/`, `backend/package.json`, `backend/package-lock.json` to recovery `archived/legacy-express/`; `backend/env/` to `archived/obsolete-python-env/`. Process/reference checks confirmed isolation before moving. Use **backend/.venv**, never the retired Express/Mongo startup. Pre-cleanup docs are retained in the full snapshot; affected canonical archive-link originals also have copies under `archived/documentation/`.

Documentation updated: root README/AGENTS, backend README; docs ARCHITECTURE, DATABASE_SCHEMA, FEATURES, MVP_SCOPE, DEPLOYMENT, SECURITY, DECISIONS, IMPLEMENTATION_PLAN, TASKS, PROJECT_STATUS, TESTING, CHANGELOG, AGENT_HANDOFF and documentation index. Canonical redirects/planning pages with private Markdown links now use archival identifiers: REVIEW_PASSES, PRODUCT_VISION, SYSTEM_DESIGN, APPROVAL_SUMMARY, REPOSITORY_PLAN, DESIGN_SYSTEM, PROJECT_ANALYSIS, SKILLS, CONTRIBUTING and USER_FLOWS. Historical folders themselves remain preserved. Final private file delta enumerates exact changes relative to the starting dirty tree.

## Database and functionality

No model, migration or database content change. Original `backend/db.sqlite3` remains content **0004**, SHA-256 `3c3252fef33ff6cec64e2c5a0eb52842ebf69abb14099c809db9298e2bab9387`.

| Existing database | Content migration | SHA-256 |
|---|---|---|
| `.local/demo/demo.sqlite3` | 0008 | `4044eb53073dc03ffb37e24ab5b3d8c7c4c5b7067d29f0adbcbf5f7db8040ecf` |
| `.local/demo-before-seed-proof/demo.sqlite3` | 0005 | `3356e13feff2b9d0e5be7688ce102152fc8dc803ae888d658051161ff8af563f` |
| `.local/sample-content-v1/demo.sqlite3` | 0008 | `684b4dc81f38fff76a669c35c86742684a11a68783d8a675714bf0ef27826eb6` |

All four SQLite files pass integrity/FK checks. Existing 0001–0008 schema applied only to fresh disposable demo/test databases; no new migrations. PostgreSQL is the normal application target; SQLite is explicit test/demo/archive only. No real transfer/cutover. Learner features remain closed for all identities. Safe HTML/Markdown, Admin workflow, approved linking/tags/related content, stateless practice, PDF reading and mock Tutor remain covered by regression tests.

The preserved sample retains 142 original syllabus IDs/five subjects, 15 published leaf lessons (6,754 words), 75 canonical questions/300 choices, 19 controlled tags, 15 aliases, 30 approved links/relations and 30 publications including ancestors. No learner or AI-usage rows are seeded. README gives startup; ADMIN_WORKFLOW gives the catalogue. Seed only a NEW private destination; never reset an existing demo. Engineering sample approval is not human academic/rights approval.

## Actual verification and release state

Original checkout and clean disposable release export: frontend **80 passed**, lint/build passed; backend **121 passed, four PostgreSQL-only skipped** (125 discovered); Django system/migration checks passed. Fresh `npm ci`, hash-locked Python installation and `pip check` passed. Chromium: **15 fixture + nine Django/Admin/PDF/mock + four sample = 28 passed**, no failures/skips. Sample API: **97 query-only checks**; five deduplicated 15-question pools grade all 75 correctly. **29 automated accessibility scans**, zero violations. Git diff whitespace/fsck and local/release docs checks passed. Detailed commands/logs/limits: TESTING.

`scripts/release_manifest.py` validates **223** source/config/test/canonical-doc inputs, including previously untracked Phase 1–4/sample source, migrations and assets. It excludes private credentials/databases/media/history/dependencies/output. Known private values were absent from release inputs. `release-copy/` installed and ran from these inputs, without private source databases/.env. **This is a worktree manifest export, not a Git commit or proof that a clone of current HEAD contains the work.** Required untracked files remain unstaged; an approved release must include the full manifest and review its diff. Never stage automatically. No remote repositories or remotes changed; remote CI has not been run.

New count tests pass; screenshot script was linted but not executed. PostgreSQL-only tests require an explicitly isolated disposable target and were skipped. No live Gemini, advisory vulnerability audit, production-host/load, physical device or manual screen-reader validation is claimed. Historical logs/results are not current defects or fresh verification.

## Blockers and exact next task

Stop after local verification. **Next task: owner reviews the local release manifest/diff and verification report, then separately approves any Git release operation or supplies the Phase 5 brief and acceptance criteria.** Do not infer or begin Phase 5.

Production gates remain: private PostgreSQL destination/roles/TLS and durable restore proof/real-cutover approval; domain/hosts/CSRF/proxy/static/private-media configuration and host validation; independent academic/rights review; live provider model/billing/rate/cap checks. PDF parsing can run 60s while proxy/Gunicorn are 40s/45s; fix only under separately approved scope. Uploaded PDF view/download is verified; topic-note PDF export is missing. No public readiness, live AI quality or completed Phase 5 claim.
