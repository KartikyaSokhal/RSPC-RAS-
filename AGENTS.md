# Prepal repository instructions

This directory is the application Git root; origin is `git@github.com:KartikyaSokhal/RSPC-RAS-.git`. Preserve the parent wrapper and its inactive Git backup. Read [handoff](docs/AGENT_HANDOFF.md), [status](docs/PROJECT_STATUS.md), [scope](docs/MVP_SCOPE.md), [roadmap and checklist](docs/IMPLEMENTATION_PLAN.md), then relevant API/Admin/security documentation before edits.

## Current authority

The owner approved only the exact documentation cleanup: privately archive 12 retired documents, edit the 16 approved paths, consolidate active requirements, and verify locally. No application refactoring, extra deletions, database migrations, production changes, credential changes, staging, commit, push, merge, history rewrite or deployment. Leave the index unchanged and stop with the proposed next commit after verification. This supersedes the earlier conditional Phase A commit instructions; that commit already exists as `49407b2`.

Release publication remains blocked pending owner review of the cleanup/security findings. No automatic continuation into master Phases B–F. Those phases retain independent push, paid-provider, data/cutover, infrastructure and deployment approvals. The current retired Django key remains disclosed in old history and the audited remote main tree; never print or reactivate it. Never rotate production secrets without approval.

## Application and data boundaries

Keep React/Vite, Django/DRF, Django Admin and PostgreSQL as the normal database. SQLite is only the immutable original archive or explicitly isolated test/demo backend. Preserve all original IDs/slugs/records/media, migrations 0001–0008, demo databases, credentials, private recovery/evidence and dormant learner implementations. No reset, clean, data rewrite or automatic fallback to original SQLite. Inspect existing databases only through read-only URI connections.

All learner registration/login/status/logout, dashboard, bookmark, progress, saved-attempt and report routes remain closed for every identity. Admin staff authentication and superuser staff-account management remain. Public reading/search/files/practice require current publication/review eligibility. SafeHtml is the browser HTML boundary; AI uses raw-HTML-disabled SafeMarkdown. Never fall back to drafts.

Content linking preserves stored HTML and evidence-bound editorial decisions. Analyze in Admin/management workflows, never student GET. Revalidate snapshots/revisions, approved proposals/aliases/tags, target and ancestor publication. Use the reviewed canonical collection service for public practice, never its draft-inclusive Admin counterpart. Grading is stateless.

UI requirements are in ARCHITECTURE: preserve original unfiltered hierarchy numbering and slug routing, all-node/root-only expansion, honest statistics, existing light/dark tokens, accessible popups and one bottom-right Tutor launcher. Do not activate learner controls. Strict current-topic Tutor and topic-note PDF export remain future Phase C work.

## Verification and release hygiene

Use `backend/run_tests.py` with isolated configurations, mocked AI and synthetic data. Never point it at real data. PostgreSQL tests need a specifically approved disposable local target. Do not run migration or demo-preparation commands during this documentation batch; only the mandated automated tests may create their own disposable fixtures internally. Report actual passes/skips/limits and distinguish local/mock checks from remote/production evidence. Never print prompts, records, keys or passwords.

Existing sample setup is documented in README. Future preparation uses a NEW private destination, refuses existing paths/symlinks/populated databases, and must not reset a failed/manual demo. Engineering review flags are not human academic/rights approval. The verifier uses query-only mode. Preserve existing demos and media.

Canonical docs stay trackable; private history/evidence/design/proposals, databases/.env/media/dependencies/output stay excluded. Run `scripts/check_docs.py --release`, `scripts/release_manifest.py`, diff and secret checks before proposing a release. A worktree export is not a commit. Use the existing documentation index instead of recreating redirect files or duplicate handoffs. Keep significant decisions in DECISIONS/CHANGELOG; private archives retain complete originals.
