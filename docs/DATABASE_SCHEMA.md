# Current database schema — student platform

Current source ends at content **0012**. Migrations 0001–0008 are byte-identical. Original backend/db.sqlite3 remains at 0004; all existing demo databases/media remain unchanged. Only new isolated review/test targets were migrated. Normal PostgreSQL configuration and historical foundation evidence follow below; historical counts describe those earlier schemas, not the current release.

| Migration | Additions/constraints |
|---|---|
| 0009 | StudentIdentity: User one-to-one, unique normalized email, nullable unique Google subject. AuthRateWindow: unique HMAC key, counter and creation index. No legacy user/data backfill. |
| 0010 | UserProgress.last_visited_at nullable/indexed; completion and visits remain distinct. |
| 0011 | Topic.estimated_study_minutes nullable 15–2400; owned StudyPlan, selected Topic M2M, weekdays/daily/default estimates/dates/revision. StudyTask retains topic/title snapshot, stage/date/minutes/sequence/completion timestamp; positive minutes, unique plan/sequence and lookup indexes. |
| 0012 | QuizAttempt immutable JSON snapshot, UUID submission ID/request digest, nullable collection topic; unique owned submission, user/time index. Quiz FK PROTECT preserves history. |

Existing Bookmark/UserProgress conditional user/topic uniqueness remains; user=NULL records are neither assigned nor exposed. New saved attempts snapshot text/choices/answers/explanations and classification while retaining canonical IDs. Legacy attempts honestly retain empty snapshots. Reversing 0009–0012 preserves legacy records but discards the new module tables/fields: back up all newly entered student work first. Reversal is a disposable-test capability, not a production rollback authorization.

New SQLite column operations reuse the existing sequence-preserving migration operation. Disposable PostgreSQL forward/reverse tests preserve original owned and ownerless bookmarks/progress/attempt IDs/fields. A fresh copy migrated 0004→0012 and preserved all 18 original tables/437 rows/columns/IDs/high-water counters with clean integrity/FKs. Synthetic transfer/restore includes identity, limiter, plan/M2M/task and attempt snapshots; actual results are in [TESTING](TESTING.md).

---

# Phase 3 schema (current)

Additive reversible migration `0008_connectionscan_keywordlinkproposal_tag_is_public_and_more` adds ConnectionScan (publication FK, pending/age, revision/hash, derived active_links JSON) and KeywordLinkProposal (stable Topic FKs, phrase/context/occurrence JSON, evidence hash/revision and review decision). It adds Tag.is_public default false, alias status/topic and pending scan/proposal lookup indexes. Existing publications receive pending scans, not automatic approvals. Existing tag labels/slugs/associations remain; no tag becomes public automatically.

No Topic, Question, Choice, Quiz or learner model is rebuilt. Original migrations 0001–0007 remain unchanged. The Tag column operation preserves SQLite deleted-ID counters in both directions. PostgreSQL and SQLite 0007 → 0008 → 0007 → 0008 tests preserve prior tags, associations, PKs and counters. Rollback removes Phase 3 proposals/plans/public-tag flags, so back up new metadata first; no rollback was performed on valuable data.

The original SQLite archive remains content 0004 and byte-identical. A new backup/copy genuinely ran 0005–0008 and preserved all 437 original rows/columns/IDs/counters; a separately migrated local PostgreSQL target matched 34 tables / 518 post-migration rows / 32 sequences. A populated synthetic transfer matched 34 tables / 193 rows, including approved proposal/plan JSON, reviewer/timestamps and one media file. Earlier 32-table/Phase 2 figures below are historical. Real PostgreSQL cutover remains unapproved.


# Historical Phase 2 additive schema

Migration `0007_tag_question_primary_topic_question_related_topics_and_more` adds Tag and TopicAlias, Topic draft tags/editorial state, TopicPublication released tags, TopicRelation review status and Question primary/related/tags associations. No duplicate Topic/Content/Question model is introduced. Unique normalized registry names and tag slugs are enforced by the database; forms/model saves normalize Unicode NFKC/whitespace/casefold. Administrative registry changes must use validated model/form saves, not raw bulk updates.

Existing questions receive quiz.topic as their primary FK. Original question/choice/quiz/attempt fields and IDs are untouched. Only matching edges present in an existing current/previous reviewed snapshot acquire approved status; all other existing edges remain draft. New tags and aliases are not inferred from stored text. PostgreSQL reverse migration removes Phase 2 fields/tables while retaining legacy rows; reversing necessarily discards newly entered Phase 2 metadata, so back it up first. No rollback ran against real data.

Both forward/reverse field operations preserve SQLite deleted-ID high-water marks during table rebuilds. Original migrations 0001–0006 are unchanged. The real SQLite file remains at 0004 with its original hash; isolated copies ran through 0007. Current source-data transfer compares 32 tables / 507 rows / 30 sequences; 437 original rows/IDs/counters remain intact. A populated synthetic transfer compares 32 tables / 177 rows and verifies all six new registry/M2M tables plus one media file. Actual commands/results are in [TESTING](TESTING.md). The following Phase 1 account is retained as historical foundation evidence; its 26-table counts describe that earlier schema.

# PostgreSQL foundation and data-preserving migration

Phase 1 makes PostgreSQL the primary application configuration. The original `backend/db.sqlite3` remains an archive at content migration 0004; application settings reject that path. No original migration file (0001–0006) is changed. The real cutover is not performed.

## Assessed data and schema

20 October 2026 source inventory: 142 Topic, 6 ContentBlock, 2 Quiz, 2 Question, 8 Choice, 5 QuizAttempt, 2 UserProgress and 0 Bookmark rows. SQLite integrity is ok with zero FK violations. Baseline SHA-256 is `3c3252fef33ff6cec64e2c5a0eb52842ebf69abb14099c809db9298e2bab9387`. Earlier documents' `035b...` hash is historical, not this phase's baseline.

0005 adds publication snapshots, relations, resources/pages, review fingerprints and budget tables plus ContentBlock source/alternative-text fields. 0006 adds nullable user ownership and conditional per-user uniqueness. Applying both to a disposable copy preserves every old column/row/PK and historical ID counter; ownerless records remain unassigned. No draft content is rewritten or automatically approved.

## PostgreSQL configuration

Normal settings use `core/database.py`: `DATABASE_ENGINE=postgresql` is default. Supply `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` and `POSTGRES_SSLMODE` through a private environment. Production requires a password and `verify-full`; set a trusted CA/`POSTGRES_SSLROOTCERT` as appropriate. No credentials are placed in source. See [environment example](../backend/.env.example) and [deployment](DEPLOYMENT.md).

Driver: hash-pinned psycopg[binary] 3.3.6. Local verification used PostgreSQL 17.11. [Django database support](https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes) and [psycopg installation](https://www.psycopg.org/psycopg3/docs/basic/install.html) are primary references.

`core.test_settings` uses SQLite :memory: without .env or migrations. `core.postgres_test_settings` uses real migrations in a newly created local `test_prepal_*` database; it requires `PREPAL_TEST_POSTGRES=1`, a `prepal_test_*` base database and loopback host. It refuses an existing test DB. The test role needs CREATEDB; the production runtime role should not.

`core.demo_settings` explicitly uses synthetic SQLite; `PREPAL_DEMO_ROOT` selects a new private demo directory. Existing demos are never reseeded or migrated by the preparation script. This is a fixture backend, not the primary application database.

## Rehearsal procedure (never a cutover command)

With explicit local PostgreSQL environment values, an empty-capable local role and frozen source/media writes:

```sh
backend/.venv/bin/python scripts/rehearse_postgres.py \
  --sqlite-source /absolute/path/to/Prepal/backend/db.sqlite3 \
  --source-media /absolute/path/to/Prepal/backend/private-media \
  --new-directory /absolute/private/new-phase1-rehearsal
```

The script refuses remote hosts or an existing directory, and creates a new random `prepal_rehearsal_*` database. It never migrates or writes the original SQLite file. It:

1. Takes a read-only SQLite backup, copies private media and verifies an independent restore.
2. Copies the restored database again and genuinely applies pending migrations. Checks all original fields/IDs, FK integrity and sequence high-water marks.
3. Applies the full schema migration graph independently to an empty PostgreSQL database.
4. Requires source/target migration graph equality. Replaces only the fresh target's generated metadata, then transfers every concrete field, including explicit auth/attempt M2M table IDs. It bypasses auto_now/save hooks so historical timestamps remain exact.
5. Imports source content types, permissions, users, sessions, groups, logs and migration-recorder IDs/dates. The target's actual pre-import migration execution history is retained separately in the private report; no migration is faked.
6. Checks deferred FK constraints and compares counts plus canonical hashes for all 26 tables, including all fields/PKs. Restores/verifies 24 sequences using historical counters, not merely current max IDs.
7. Tests administrative login/publish/withdrawal, public reading, reviewed stateless grading and authenticated/guest containment using synthetic rows inside a rolled-back transaction. Resets sequence counters after those checks and rechecks imported data.
8. Rechecks the original source hash/inventory and writes a private result manifest without raw records or credentials.

Current rehearsal: 437 original non-migration rows preserved across the source migration; 496 total rows in 26 migrated tables transferred exactly, including newly generated framework metadata and migration records. No publication/review/resource rows are invented for the real corpus. A separate all-type synthetic transfer tests Unicode/JSON, files, framework rows, M2M IDs and deleted-ID counters of 9000/9001.

## Recovery and approval

Native PostgreSQL custom-format dump/restore was independently rehearsed into another fresh local database. `scripts/verify_postgres_restore.py PRIVATE_RESULT_JSON` reads the restored target, compares every table and sequence to the rehearsal manifest, and checks constraints; it does not perform restore or cutover. Set the explicit rehearsal environment and migrated-copy path as described in [deployment](DEPLOYMENT.md).

The SQLite archive, private backup/media and code/config baseline remain the recovery sources. Do not switch current code to the unmigrated archive as an automatic fallback. Rehearsal artifacts in temporary directories are not a durable backup policy. Final destination, TLS, least-privilege roles, durable backup storage and the actual cutover require owner review/approval. See verified results (retained privately as `docs/evidence/PHASE_1_VERIFICATION.md`).

## Module 4 — deterministic study planning

Local planner implemented with owned plans/tasks, selected published branches, Monday=0 days, daily capacity and approximate admin estimated_study_minutes per topic. Default 90 minutes is editable per plan; learning allocates 60/20/20% to learn/revise/practice, quick revision halves total (minimum 15), allocated 20/50/30%. Schedules split across chosen days, report exam feasibility and weekly/monthly subject totals. Edits/rescheduling preserve completed task IDs/timestamps and replace unfinished tasks; task completion is separate from marking a whole lesson completed. Migration 0011 is additive and not applied to existing data. Focused student backend: 30 passed. Production gate remains off by default.

## Current PostgreSQL student preparation — 23 October 2026

No model or migration was changed in this task. Schema0001–0012 was genuinely applied to NEW disposable PostgreSQL targets; original SQLite/demo files were not migrated. StudentIdentity→User and owned Bookmark/UserProgress/QuizAttempt/StudyPlan→User, StudyTask→StudyPlan remain the same existing relationships. NULL-owner legacy rows are never assigned automatically.

Actual8002 settings: core.student_demo_settings. Source is ../.recovery/prepal-student-platform-yeqsw05q/student-review/demo.sqlite3 (SQLite), media sibling media/. At preflight: one synthetic staff editor; zero student identities/nonstaff users/sessions/bookmarks/progress/attempts/plans/tasks;142 topics,200 questions,800 choices. Source backup restored40SQLite tables including sqlite_sequence. A restored copy, not the running DB, supplied the PostgreSQL rehearsal:39 application tables/2,433 rows, exact fields/IDs/FKs/migration history;37 sequence high-water marks. Synthetic persistence tests then produced2,467 rows in39 tables, independently dumped/restored with37 sequences plus one synthetic media file. Session, password hash, immutable quiz and completed planner history remained usable after restore. Source/data cutover NOT performed.

Database owner/migration credentials differ from limited runtime and read-only backup roles; new local provisioning revokes PUBLIC database access and public-schema creation. Production needs approved host/CA and verified TLS/role/backup acceptance. The local16.2 binary has no SSL support. No synthetic staff/accounts/publication decisions may be transferred into production without explicit approval.
