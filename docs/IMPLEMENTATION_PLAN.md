# Master release execution — remediated Phase A

| Phase | Required action / gate | Current state |
|---|---|---|
| A | Retire historical local Django key, scan/reverify exact release; create owner-approved local commit | Remediation and verification complete; approved message: Prepare Prepal content-first MVP release baseline |
| B | Separate push approval; remote SHA and CI verification | Pending owner approval; SSH read access verified, gh CLI unauthenticated |
| C | Published-topic PDF export and server-enforced current-topic Tutor | Not started |
| D | Approved PostgreSQL source/target/roles/TLS/durable encrypted backup and cutover | Not started |
| E | Approved provider/domain; production proxy/static/private media/monitoring; PDF timeout alignment | Not started |
| F | Approved staging and restore/security verification, then separate production approval | Not deployed |

The approved candidate has 223 release files and only the two starter SVG deletions. Remediation changes existing documentation and ignored backend/.env only. No migrations/model/dependency/runtime implementation edits. Verified backup/checkpoint protects the reviewed candidate and original environment. Independent generation replaced the exposed development key; no fallback, history rewrite, production credential access, data write, push or deployment. Exact checks/limits and Git revision lookup: AGENT_HANDOFF/TESTING. Earlier maps below are historical.

---

# Controlled cleanup implementation — current

| Change | Exact files |
|---|---|
| Honest hierarchy/search counts | `src/pages/syllabusPage.jsx`, `src/pages/searchPage.jsx`, `src/test/counts.test.jsx` |
| Seven unused imports | `backend/content/admin.py`, `views.py`, `services/connections.py`, `discovery.py`, `practice.py`, `pdf_extract.py` |
| Private capture/config clarity | `scripts/capture_admin_screenshots.mjs`, `backend/gunicorn.conf.py` |
| Trackable canonical docs / IDE visibility | `.gitignore`, `.vscode/settings.json`, `prepal.code-workspace` |
| Release/export/document checks | `scripts/release_manifest.py`, `scripts/check_docs.py`, `.github/workflows/checks.yml` |
| Verified removal/archive | Unused starter SVGs; generated caches/Finder metadata/stale dist; privately archived retired Node backend and old Python environment |

Exact next task after local verification: owner reviews cleanup/release evidence, then supplies separate publication/production or Phase 5 scope and approval. Do not commit, push, deploy or perform real cutover automatically. Earlier phase maps below are historical context.

---

# Sample content population — completed locally

| Work | Files | Acceptance |
|---|---|---|
| Original academic corpus | `backend/content/fixtures/sample_lessons_v1.json` | 15 existing leaves, 428–480 note words, 75 four-option questions/explanations, verified references, controlled tags/connections |
| Exclusive isolated preparation | `scripts/prepare_sample_demo.py`, `backend/content/management/commands/create_sample_content.py` | New directory and marker; populated/repeated destinations refused; existing schema only; normal review/publication services |
| Read-only validation | `backend/content/services/sample_content.py`, `scripts/verify_sample_demo.py` | Exact hierarchy, counts, sanitized snapshots, tags/links, no duplicates, 15 questions per subject, deterministic grading; no learners/provider requests |
| Regression coverage | `backend/content/test_sample_content.py`, `e2e-sample/content.spec.js`, `playwright.sample.config.js`; npm/eslint scripts | Safety/refusal tests, browser corpus/tag/popup/practice acceptance, existing suites preserved |
| Documentation | Existing README/backend README/AGENTS and scope, architecture, features, Admin workflow, decisions, plan, tasks, status, testing, security, changelog, index and handoff | Actual results, startup commands, corpus catalogue, approval meaning and exact next task |

This is supplemental demo population, not Phase 5. Next: owner reviews sample material and supplies a separate Phase 5 scope/approval. No real cutover, learner activation, paid calls or deployment.

---

# Phase 4B implementation map (current)

Approved source: owner’s Phase 4A map and Phase 4B brief in the conversation. Targeted frontend work only; original uncommitted phases remain.

| Work | Exact files | Acceptance |
|---|---|---|
| Shared hierarchy/counts | `src/components/study/syllabusContext.js`, `syllabusUtils.js`, `src/hooks/useSyllabus.js`, `src/components/layout/AppShell.jsx`; Home/SyllabusPage/TopicPage callers | One shared request; all API roots/descendants counted; honest loading/error states |
| Stable tree | `src/components/study/SyllabusTree.jsx`, `src/App.css`, `src/styles/study.css` | Original-order 1/1.1/A numbering under filters; all-node expand; root-only collapse; individual keyboard toggles after each |
| Homepage | `src/pages/home.jsx`, `src/App.css` | Compact undistorted map; only Explore Syllabus hero action; accurate assistant copy; two statistics; API-root jump/focus buttons; loading/error/retry retained |
| Navbar/footer | `src/components/layout/AppShell.jsx`, `src/App.css` | Logo left; Search/theme right at all widths; no center/auth/About navigation; retained branding/dynamic totals; empty noninteractive social space |
| Reader Tutor | `src/pages/topicPage.jsx`, `src/styles/study.css` | One bottom-right launcher; no toolbar/mobile duplicates; nonmodal Escape/close/focus restore; responsive two-column reader; Phase 3 preserved |
| Tests | `src/test/auth-dashboard.test.jsx`, `ui-foundation.test.jsx`, `uiHierarchy.js`, `e2e/ui-foundation.spec.js`; existing suites retained | Header/theme, counts/retry, original numbering, toggles, focused subject navigation, Tutor and Phase 3 safety; widths 320/390/768/1024/1280 |
| Documentation | README/AGENTS and existing architecture/features/scope/decisions/plan/tasks/status/testing/changelog/handoff | Actual results, exact delta, source preservation, remaining limits and Phase 5 gate |

Exact next task: obtain owner’s Phase 5 scope, acceptance criteria and explicit approval. Do not implement Phase 5. Real cutover, paid-provider and launch approvals remain separate.

---

# Historical Phase 3 implementation map

| Work | Exact files |
|---|---|
| Proposal/queue/public-tag schema | `backend/content/models.py`, `migrations/0008_connectionscan_keywordlinkproposal_tag_is_public_and_more.py` |
| Matching/review/derived plans | `backend/content/services/connections.py`, `signals.py`, `apps.py`, `admin.py`, `management/commands/regenerate_connections.py`; publication/restore hooks in `services/publication.py` |
| Public discovery and collections | `services/discovery.py`, `services/collections.py`, `services/practice.py`, shared grading in `services/quiz.py`, `views.py`, `urls.py` |
| Safe reader UI | `src/components/content/SafeHtml.jsx`, `components/study/ContentRenderer.jsx`, `TopicPopup.jsx`, `pages/topicPage.jsx`, `styles/study.css` |
| Tag/practice pages | `src/pages/tagPage.jsx`, reused `quizPage.jsx`, `src/App.jsx` |
| Acceptance/compatibility | `backend/content/test_discovery.py`, latest-graph restoration in `test_phase2.py`, synthetic `create_demo.py` and `scripts/verify_postgres_transfer.py`, `src/test/discovery.test.jsx`, `e2e-integration/discovery.spec.js`, targeted existing journey selector |
| Current evidence/authority | README/AGENTS/backend README and existing scope/architecture/features/Admin/API/database/security/AI/deployment/decisions/tasks/status/testing/index/handoff documents |

Exact next task: obtain the Phase 4 scope, acceptance criteria and explicit approval. Do not implement Phase 4. Separately pending: real target/roles/TLS/media/durable recovery decisions, source freeze/backup/cutover approval, real corpus review and paid model/rates/cap. The Phase 2 map below is historical and its stop-before-Phase-3 instruction is superseded only by the current approved Phase 3 scope.


# Phase 2 implementation map and next task

The approved content-management foundation extends the Phase 1 content-first/PostgreSQL architecture. No real cutover or Phase 3 implementation is authorized.

| Work | Exact files | Result |
|---|---|---|
| Controlled registry and associations | `backend/content/models.py`; `migrations/0007_tag_question_primary_topic_question_related_topics_and_more.py` | Unique normalized Tag/TopicAlias; draft/publication tags; relationship review state; Question primary/related/tags; reversible legacy-primary backfill; SQLite counter preservation |
| Existing CMS workflow | `backend/content/admin.py`, `forms.py`, `templates/admin/content/topic/change_form.html`, `static/admin/js/prepal_wysiwyg.js` | Topics/Content/Practice Questions; permissions; draft/review/preview/publish/withdraw; draft-only block saves; PDF preparation feedback; untouched blank-inline fix |
| Released content boundary | `backend/content/services/publication.py` | Freeze tag metadata on explicit publish/restore; include only approved edges; suppress revoked snapshot edges centrally |
| Canonical MCQ collections | `backend/content/services/collections.py`, `services/quiz.py` | Bounded syllabus traversal, distinct existing question IDs, reviewed default eligibility, deterministic metadata-bound fingerprints |
| Tests and synthetic fixtures | `backend/content/test_phase2.py`, `test_admin_redesign.py`, `test_ai.py`, `test_mvp.py`; `management/commands/create_demo.py`; `scripts/verify_postgres_transfer.py`; `e2e-integration/admin-content.spec.js` | Actual backend/migration/Admin/browser/transfer regressions; mock services and separate databases |
| Documentation | README/AGENTS/backend README; architecture/database/API/Admin/security/testing/status/tasks/features/scope/decisions/changelog/index/handoff | Current behavior, compatibility, evidence and remaining approval gates |

**Exact next task: Phase 3 dynamic content linking and discovery.** Wait for owner approval before implementing it. Review approved aliases/edges and canonical tags as inputs; decide matching ambiguity, publication/revocation and discovery rules before adding links. AI-generated tags, automatic keyword insertion, public tag discovery, student identity/dashboard/planning, homepage redesign and Tutor changes were excluded from Phase 2.

Real PostgreSQL cutover remains an independent approval gate: select destination/roles/TLS/private media and durable backups, review a fresh source freeze/restore/rehearsal, then obtain explicit authorization. Phase 2 verification does not approve real content or its rights. Historical Phase 1 implementation and commands remain in its unchanged evidence and changelog.

---

The following is the preserved pre-Phase-2 implementation map. Its statements about authorization are historical; the current Phase 2 brief and map above govern.

# Historical Phase 1 implementation map (superseded approval boundary)

The approved Phase 1 content-first/PostgreSQL brief supersedes the previous learner-enabled milestone map. Historical scope changes remain in [decisions](DECISIONS.md), [changelog](CHANGELOG.md) and earlier evidence. No Phase 2 feature is authorized here.

| Work | Exact implementation files | Current result |
|---|---|---|
| Database selection | `backend/core/database.py`, `settings.py`, `test_settings.py`, `demo_settings.py`, `postgres_test_settings.py`, `rehearsal_settings.py`; `backend/.env.example` | PostgreSQL default; explicit isolated SQLite; source path/production fallback refused |
| Driver baseline | `backend/requirements.in`, `requirements.txt`, `requirements-dev.txt` | Hash-pinned psycopg/binary added; existing versions retained |
| Transfer and recovery | `backend/content/services/database_transfer.py`; `scripts/rehearse_postgres.py`, `verify_migration.py`, `verify_postgres_transfer.py`, `verify_postgres_restore.py` | Real migrations, exact concrete/M2M fields and metadata, source/copy checks, sequences, native restore |
| API containment | `backend/content/urls.py`, `permissions.py`, `views.py`, `services/publication.py` | Every learner/auth route unavailable for every identity; no public learner-state lookups |
| Student UI containment | `src/App.jsx`, `pages/learnerUnavailablePage.jsx`, `pages/topicPage.jsx`, `components/layout/AppShell.jsx`, `learnerFeatures.js` | No student provider/forms/links/probes; unavailable routes and disabled controls |
| Existing Admin safety | `backend/content/admin.py`, `test_admin_redesign.py` | Existing authoring/tree/WYSIWYG preserved; reports closed; staff-only account management; explicit PDF review |
| File boundary | `backend/core/urls.py`, `services/publication.py`, `vite.config.js` | No raw private-media route/proxy or unreviewed legacy attachment link; stored files/records retained |
| PostgreSQL quota correctness | `backend/content/services/ai_budget.py`, `test_postgres.py`, `scripts/verify_budget_race.py` | Conditional global reservation and idempotent row-locked settlement; no provider calls |
| Test isolation/compatibility | `backend/run_tests.py`, `core/test_runner.py`, `content/test_database.py`, `test_auth.py`, existing baseline/quiz/MVP/operations tests; frontend containment tests; Chromium specs; `playwright.integration.config.js`, demo preparation/command | SQLite + PostgreSQL regressions; separate browser demo/ports; original databases excluded |
| CI | `.github/workflows/checks.yml` | PostgreSQL service/testing/transfer prepared; remote execution unverified |
| Documentation | README, AGENTS, backend README and active scope/status/tasks/API/security/database/deployment/testing/architecture/Admin/decision/changelog documents | Current release boundary and actual evidence recorded |

Verified: PostgreSQL local target and native backup/restore, original SQLite byte/row/ID preservation, administrative workflows, approved stateless practice and learner containment. See actual results (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).

Remaining Phase 1 gate: owner reviews the rehearsal and selects the real destination, least-privilege roles, private credentials, TLS/media/durable backups, then explicitly approves a fresh cutover. Current scripts are rehearsal-only and will not migrate a valuable source or remotely deploy.

Future work is deferred: student release, new editor/tagging/link features and other Phase 2 expansion need separate approval. Real content/rights review and target-host validation are launch conditions, not implied by fixture tests.
