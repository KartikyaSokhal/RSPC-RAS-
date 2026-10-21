# Current status — remediated and approved Phase A baseline

Branch **codex/prepal-1-0**. Verification/base commit **ee272a6954868b303447545eb553200adb024a24**; release revision is the commit containing this handoff, resolved by `git log -1 --format=%H -- docs/AGENT_HANDOFF.md`. Approved message: **Prepare Prepal content-first MVP release baseline**. The owner authorized local commit after remediation; no push, remote change, deployment or real PostgreSQL cutover.

The exposed Django key was active only in the scoped local development .env. Rotation is complete, with a new random key, private permissions and no fallback. Nine focused checks pass; old sessions/signatures expire without changing passwords/data. The retired key remains in two old commits, including current remote main; no history was rewritten. No additional active credential exposure was found in Gitleaks or exact-value staged/history scans. External reuse/visibility remain unverified; production credentials were not accessed.

Fresh verification: **80 frontend passed**, lint/build passed; **121 backend passed/four PostgreSQL-only skipped**, **nine rotation checks passed**, Django/migration checks clean. All **223 release inputs** remain complete. Of 162 previously protected files, only backend/.env intentionally changes; the other **161 hashes remain unchanged**, including all four databases, media, models/migrations and locks. Original SQLite stays content 0004; demos stay 0008/0005/0008. Earlier browser/clean-install results below are historical, not rerun here.

**Next:** separate owner approval for Phase B push; verify remote commit SHA and CI after any authorized push. SSH read access works; gh CLI lacks authentication. Phase C PDF export and strict current-topic Tutor, then approved PostgreSQL/hosting/staging/production work remain pending. Learner features stay disabled, no paid AI invoked, no production URL. Current details: TESTING and AGENT_HANDOFF; dated status below is historical.

---

# Project status — controlled cleanup verified locally

21 October 2026. Branch **codex/prepal-1-0**, unchanged HEAD **ee272a6954868b303447545eb553200adb024a24**, origin `git@github.com:KartikyaSokhal/RSPC-RAS-.git`. Earlier Phase 1–4B, Admin/editor and academic-sample implementations remain uncommitted and preserved. No staging, commit, push, deployment or real database cutover.

Cleanup is complete: a full private recovery archive was verified before changes; retired Express/Mongo and obsolete `backend/env` were archived outside the checkout; unused starter assets, Finder metadata and regenerable caches/stale output were removed. Active dependencies remain installed. IDE exclusions hide local/generated material. Canonical docs are trackable; private evidence/history stays excluded. Screenshot capture no longer embeds credentials. Seven unused imports were removed without changing module executable bodies. Full-syllabus/search counts no longer invent fallback totals; three new regressions cover unavailable/empty/filtered data.

**Verification:** 80 frontend tests, lint/build, 121 applicable backend tests (four PostgreSQL-only skips), Django checks/migration consistency, 28 Chromium tests, 97 sample API checks and 29 automated accessibility scans passed. A new disposable manifest export installed both dependency locks and passed the checks. It represents 223 current worktree release inputs, not a published Git checkout. CI configuration includes manifest/docs/sample checks, but remote CI was not run. Exact commands, evidence and limits are in [TESTING](TESTING.md).

**Data:** all 162 protected hashes remain unchanged. Original SQLite is at content 0004; existing demos remain at 0008 (`.local/demo`), 0005 (`.local/demo-before-seed-proof`) and 0008 (`.local/sample-content-v1`). All four pass integrity and foreign-key checks. Models/migrations/locks, media and historical evidence remain unchanged. Existing 0001–0008 migrations ran only on fresh disposable test/demo databases. No new migration was created; no PostgreSQL server/cutover was performed.

The preserved academic demo still has five subjects/142 topics, 15 original lessons, 75 MCQs/300 choices, 19 controlled tags and 30 approved links. [README startup](../README.md#academic-sample-demo--21-october-2026) and [Admin catalogue](ADMIN_WORKFLOW.md#local-academic-sample-content--21-october-2026) remain authoritative. Engineering approvals are not independent academic/editorial approval. Learner features remain disabled; paid AI was not invoked.

Private recovery/evidence: `../.recovery/prepal-cleanup-20261021-d8aem1mu/`; the archive, final release manifest and protected-hash report are retained there. Exact files and recovery boundaries are in [AGENT_HANDOFF](AGENT_HANDOFF.md).

**Next task:** owner reviews this local release and separately approves any commit/push or production preparation. Phase 5 requires its own brief, acceptance criteria and approval. Remaining production blockers: PostgreSQL roles/TLS/private media/durable recovery and real cutover approval; domain/proxy/static settings and host validation; content/rights review; live model/billing/cap validation; PDF request timeout alignment; and unimplemented topic-note PDF export. No deployment readiness claim is made.
