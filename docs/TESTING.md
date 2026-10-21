# Testing and verification

Current batch: approved documentation/ignore cleanup over unchanged 49407b2. Only the 12 archived removals and 16 approved edits are in scope. No application/dependency/model/migration file changes, commit/push/merge/history rewrite, paid provider or production operation. Verification below is updated only from actual executed checks.

## Current cleanup results

| Check | Actual result |
|---|---|
| Private archive/recovery | All 28 original files hash-verified; exact 12 removal copies retained; independent restore matches every member |
| Frontend tests / lint / build | **80 passed**, 10 files; lint and production build passed in private release export; fresh locked npm install passed |
| Isolated backend tests | **121 passed, four PostgreSQL-only skipped**, 125 discovered, 9.005s; run from private export with existing pinned backend environment |
| Django system/migration consistency | No issues; makemigrations --check --dry-run reports no changes; no application/data migration command run |
| Documentation links/references | File links pass in 22 local/19 release documents; retired-file references and preserved sample anchors checked |
| Secret/Git checks | Gitleaks worktree-release/history scans exit 0; no current local secret exact matches; one known retired historical blob remains; diff whitespace/fsck pass |
| Required release export | All 211 required inputs SHA-verified; 19 canonical Markdown files; no missing source/new release file/private artifact |
| Data/credentials/history/source preservation | 162 protected hashes/195 other tracked files unchanged; four SQLite integrity ok/FK0; exact 12 deletions/16 modifications; HEAD/index/branch/origin unchanged and no staged files |

Ignore tests additionally verify 21 private/generated path cases are excluded, while all 211 release paths and safe templates/public CA/SQL remain eligible. Tests/build ran outside the application checkout so its generated output/dependencies remain intact. Only mandated test internals may construct disposable fixtures; no existing/source/demo schema or data changed.

Private current evidence: ../.recovery/prepal-doc-cleanup-po2fcd2c/. It contains approved-plan.json, before/protected manifests, approved-documents-before.tar.gz, ARCHIVE_VERIFIED.json, archived copies and restore-proof, plus verification logs/final reports. Restore only to a NEW private directory; do not overwrite the checkout. Credentials/DBs were not copied into the documentation archive or changed. Prior private recovery records remain intact.

## Reproduce safe checks

Use Node 24.22.0/Python 3.14.6/Django 6.0.9 from the pinned runtime files. Tests must use isolated configurations and mocked AI. Existing mandatory tests may create disposable fixtures internally; do not apply migrations to application/original/existing-demo databases or run separate demo preparation during this cleanup.

```sh
npm run check
PYTHONDONTWRITEBYTECODE=1 PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/run_tests.py
PYTHONDONTWRITEBYTECODE=1 PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/manage.py check --settings=core.test_settings
PYTHONDONTWRITEBYTECODE=1 PYTHON_DOTENV_DISABLED=1 backend/.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=core.test_settings
PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python scripts/check_docs.py
PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python scripts/check_docs.py --release
PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python scripts/release_manifest.py
git diff --check
git fsck --full --no-dangling
```

Use release_manifest.py --export with a NEW private absolute destination to verify the current worktree's 211 explicit inputs; never add private data to make a check pass. Preserve index/HEAD; deleted paths remain pending in the uncommitted diff until an approved future staging/commit. Test ignore patterns without creating secret files; safe .env.example/templates/public CA/SQL/source/canonical docs must remain eligible.

Run the checksum-verified private Gitleaks binary with full redaction on exact release bytes and reachable history, alongside independent literal checks against current private values and the retired key. Default Gitleaks rules miss the known insecure development key; that inactive historical match is a documented finding, not a new active leak. A documented Git SHA beside a key-like label previously caused a generic-rule false positive; reworded prose fixed it without scanner suppression. Reports remain private. No scanner proves absence of every unknown/external secret.

## Optional future checks, not authorized new infrastructure

Frontend browser commands are test:e2e, test:integration and test:sample. Suites rebuild shared output and must run serially with loopback servers, the matching Chromium binary and explicitly isolated demos. Do not point mutable Admin tests at preserved data. Existing sample verify_sample_demo.py is query-only; it must not become an automatic reset. PostgreSQL-only tests require separately approved disposable loopback targets/guarded runner; no production target or implicit provisioning.

## Historical evidence (not rerun by this batch)

| Batch | Evidence actually recorded at that time |
|---|---|
| GitHub audit / clean clone of 49407b2 | Fresh locked npm/Python installs; 80 frontend, 121 backend/four PostgreSQL skips, lint/build/Django/docs, 97 sample API checks; six local commits/345 blobs and six remote commits/202 blobs; no active local credential matches |
| Phase A key retirement | Nine isolated session/reset/cookie/practice/quota checks; old key retired without fallback; passwords/data preserved; default scanner plus exact-value scope recorded |
| Earlier controlled cleanup/sample | 28 Chromium tests (15 fixtures/nine Admin-PDF-mock integration/four samples), 29 axe scans with zero violations, 97 query-only API checks and verified recovery/clean export; no live-model/physical-device certification |
| Phase 3 | 120 PostgreSQL tests on disposable target; SQLite 116 passes/four skips; migration reversal/ID-sequence/native-restore/transfer checks on copies; no real cutover/durable production proof |

No fresh browser, PostgreSQL-specific, live Gemini, vulnerability-advisory, physical-device/manual-screen-reader, remote CI, staging or production check is claimed unless the current-results table explicitly records one. There is no configured standalone TypeScript typecheck in this JavaScript app. Host process visibility may be needed by the existing bounded PDF parser guard. Independent human content/rights review, target-host/load/TLS/media/backup restoration and live-model billing/quality remain pending. [Security](SECURITY.md) and [deployment](DEPLOYMENT.md) define remaining gates.
