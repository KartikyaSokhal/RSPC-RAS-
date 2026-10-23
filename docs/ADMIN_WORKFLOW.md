# Local academic sample content — 21 October 2026

The new `.local/sample-content-v1` demo uses the existing syllabus IDs, titles, slugs and parents exactly. It contains no invented syllabus nodes. Its canonical input is `backend/content/fixtures/sample_lessons_v1.json`; preparation and startup are documented in [README](../README.md#isolated-student-review-demo).

| Original subject | Existing lesson ID and title | Reader path | Note words | MCQs |
|---|---|---|---:|---:|
| History, Art, Culture, Literature, Tradition & Heritage of Rajasthan | 30 · a. Temples | `/topic/a-temples` | 430 | 5 |
| History, Art, Culture, Literature, Tradition & Heritage of Rajasthan | 31 · b. Forts | `/topic/b-forts` | 437 | 5 |
| History, Art, Culture, Literature, Tradition & Heritage of Rajasthan | 33 · d. Man-made water bodies | `/topic/d-man-made-water-bodies` | 445 | 5 |
| Ancient & Medieval Period | 60 · ii. Buddhism | `/topic/ii-buddhism` | 443 | 5 |
| Ancient & Medieval Period | 61 · iii. Jainism | `/topic/iii-jainism` | 428 | 5 |
| Ancient & Medieval Period | 63 · a. Maurya | `/topic/a-maurya` | 460 | 5 |
| Modern Period (from early 19th century to 1964) | 93 · b. Press | `/topic/b-press` | 454 | 5 |
| Modern Period (from early 19th century to 1964) | 98 · a. Various leaders | `/topic/a-various-leaders` | 446 | 5 |
| Modern Period (from early 19th century to 1964) | 104 · a. The linguistic reorganisation of the states | `/topic/a-the-linguistic-reorganisation-of-the-states` | 435 | 5 |
| World Geography | 112 · d. Deserts | `/topic/d-deserts` | 463 | 5 |
| World Geography | 119 · b. Deforestation | `/topic/b-deforestation` | 461 | 5 |
| World Geography | 122 · e. Ozone Layer Depletion | `/topic/e-ozone-layer-depletion` | 450 | 5 |
| Geography of India | 128 · 8. Mechanism of Monsoon | `/topic/8-mechanism-of-monsoon` | 460 | 5 |
| Geography of India | 129 · 9. Rainfall Distribution | `/topic/9-rainfall-distribution` | 462 | 5 |
| Geography of India | 134 · b. Rice | `/topic/b-rice` | 480 | 5 |

Every lesson has three controlled tags, reused across lessons (19 registry entries total). There were no existing tags in the prior local demo to reuse; the new registry shares academically meaningful labels such as Water management, Ancient India and Historical sources. Each question has its existing leaf as primary_topic and derives its subject through that leaf's ancestry; no redundant subject model or copied question collection is introduced. Optional related question associations are left empty so each sample subject has exactly 15 questions. Topic relationships still cross subjects where useful.

The seeder creates 15 demo-approved quiz reviews, 15 approved aliases, 30 approved TopicRelation edges and 30 evidence-bound KeywordLinkProposal approvals through the established services. Only curated phrase/target pairs are approved. Fifteen lesson publications and their 15 necessary ancestor publications make the content eligible; remaining syllabus topics retain coming-soon behavior. Student GET does not generate suggestions or modify HTML.

**Approval meaning:** source-checked agent-authored sample content for local development, not independent human subject-expert approval, official RPSC material or production-ready editorial content. All notes carry a visible notice, practice titles start Sample practice, and QuizReview source text records this limitation. Sources include NCERT/IIT Kanpur SATHEE, Rajasthan Tourism, UNESCO, India Code, IMD, ICAR, JAINpedia, NASA, USGS and EPA. Each lesson includes reference links; hypothetical examples are labeled. No reference text or imagery is reproduced wholesale. Human academic and rights review remains required before public release.

Edit this isolated demo through the existing draft/review/publish workflow if desired. Rerunning setup must never overwrite those edits: existing destinations and completed markers are refused. The strict verifier checks the unmodified versioned fixture, so subsequent editorial changes require their own review evidence. No additional PDFs were requested or seeded; existing PDF functionality is verified with the preserved legacy fixture suite.

---

# Phase 3 linking and discovery workflow

1. Publish source and target content through the existing review workflow. Only meaningful published titles and approved aliases become candidates. Set **Approved for public discovery** on reviewed Tag records; new/existing tags default private. Assign draft Topic tags, then explicitly publish to release those associations.
2. Select published source Topics and run **Suggest Connections**. Open **Keyword link proposals** in Topics. Inspect each phrase, source, target and surrounding context; approve or reject individual rows using the Admin actions. Ordinary staff need view/change KeywordLinkProposal permissions; no permissions are granted automatically. General TopicRelation review remains separate.
3. Repeated analysis retains decisions for identical published HTML. Changed HTML produces fresh pending evidence. A stale proposal cannot be approved; old rejected/approved evidence remains for audit. Rejecting a phrase does not remove an independently approved syllabus/TopicRelation association.
4. Publication/restore scans its own source immediately and runs a bounded background batch inline in the editorial workflow (default total 20). Alias Admin saves also process queued scans. Additional work stays queued fairly by analysis age. Run `backend/.venv/bin/python backend/manage.py regenerate_connections --limit 20` with the intended isolated/approved settings until no scans remain. `--all-current` queues an intentional recheck. It never auto-approves or rewrites article HTML. Do not use the real SQLite archive as runtime.
5. Review the student popup, current published description and new-tab action. Withdrawal of a target/ancestor or alias/proposal approval removes eligibility on the next response; popup opening revalidates current context. Active browser pages are not continuously polled. Unavailable cached spans are withheld rather than replaced on student requests; regenerate editorially to fill unused slots.

Matching supports case-insensitive whole phrases, Unicode marks/casefold and variable whitespace. Longest approved overlaps win before duplicate-target suppression; maximum eight links per article. Existing links/headings/code are skipped. Phrases spanning separate inline-formatting text nodes are intentionally not joined; use a coherent phrase or a manually authored safe link. Ambiguous vocabulary is withheld for editorial correction. Existing source/formatting/resource rules below remain; earlier statements that aliases have no link behavior describe Phase 2 only.

Public tag routes use released associations and stable slugs. Subject practice references canonical questions from published branches and matching reviewed quiz containers, without copying questions. Guest checks remain stateless; the enabled student platform additionally supports owned immutable attempts.


# Content editing, review and publication

Use Django Admin. Real PostgreSQL cutover needs separate approval; isolated SQLite/PostgreSQL authoring tests are available. The current student gate is opt-in in production; content-only demos keep it closed. Administrative learner reports remain disabled while staff login works. Give real editors named staff accounts with only required content permissions; do not reuse demo credentials or share superuser access.

## Lesson workflow

1. Create parent collections first, then ordered Topic children. Existing published slugs/parents remain stable; creating a cycle is rejected.
2. Add ordered ContentBlock headings/text/images. Text accepts educational HTML; unsafe markup and inline remote images are stripped from publication. Use image blocks for validated PNG/JPEG/WebP with alt text, caption and source. Stored draft HTML is preserved.
3. Save drafts, then open **Preview draft** from the topic list. Preview is staff-only and sanitized; private image preview is permission checked. Saving drafts does not change the public version.
4. Select controlled tags on the Topic; register keywords in Topic keyword aliases with their Topic and draft/approved/withdrawn status. Approved aliases support the evidence-reviewed linking workflow above; saving one never approves every phrase. Add related/prerequisite TopicRelation entries with a useful reason and explicitly approve reviewed edges before publishing the source. Targets must independently be public. Revoking an edge suppresses it immediately in existing consumers.
5. Use **Submit for review** to mark the saved draft awaiting review; this does not publish. Review facts, claims, sources, reading order, formatting, image rights and alternatives. Select **Publish selected topics after editorial review**; publish parents before children. Public catalog/reader/search/tutor all use that snapshot.
6. Withdraw to hide the topic and descendants without deleting rows. Republish the previous approved snapshot when appropriate; this increments revision and preserves the replaced current snapshot as the previous one.

Only one previous publication is retained; this is not a full version-history CMS. Unsupported educational HTML (SVG, iframe, executable attributes, inline styles/scripts, arbitrary embedded images) must be converted to safe native notes or validated image blocks. PDF ContentBlock attachments remain stored but cannot silently bypass the resource review workflow.

## PDF workflow

Upload a LearningResource with its Topic, title, source reference and rights note, either inline in Topic editing or through the resource administration page. Existing inline preparation is retained; successful extraction leaves it `ready`, not approved, and never republishes the topic automatically. PDF extension/MIME/magic/20 MB checks run at upload. Run `backend/.venv/bin/python backend/manage.py process_resources` using the intended isolated or approved production settings. The bounded command handles at most 20 candidates, with three attempts and stale-claim recovery.

Open the resource's **Inspect private source PDF** and **Review extracted pages** links after processing. Compare page count/order and text with the original; identify scanned pages and extraction mistakes. Encrypted/active/invalid files fail; pages without enough text become `needs_ocr` and cannot be approved. No paid OCR is used. Approved/processed candidates cannot be silently overwritten in Admin; upload a new candidate for revisions.

Approve only `ready` resources with verified source/rights. Then publish the topic to explicitly include the approved resource. Withdrawal immediately removes public file and search access. PDFs are excluded from the current-lesson Tutor evidence. Raw private-media links are never publicly routed. Historical ContentBlock attachments remain stored but are withheld from public reading until represented by an explicitly reviewed LearningResource. This is an intentional compatibility restriction; no original file or record is deleted.

## Quiz workflow

Create Quiz and canonical Questions; select a primary leaf subtopic and optional related leaf subtopics/tags, then open each Question to add choices. Do not duplicate a question to include it in a subject collection: use the **Syllabus question collection** filter in Questions. It includes primary and related descendants once per question, including drafts for authoring. The reviewed collection service excludes unpublished/unreviewed questions. Existing backfilled ancestor locations may be retained, but new/moved locations must be leaves. Provide at least two nonempty choices, exactly one correct choice and an explanation for every question. Create a QuizReview with a source reference, review all items, then use its approve action. The review fingerprint covers ordered quiz content and nonlegacy primary/related/tag associations. Default legacy primary backfills preserve existing approvals. Editing a question/choice/explanation makes the quiz unavailable until re-reviewed. A temporary environment allowlist cannot override this boundary.

Practice checks score +1 correct, 0 wrong/unanswered, with no negative marking or timer and no saved guest attempt. This is not an official examination scoring claim.

## Reusable lesson template and release corpus

Title → learning objectives → introduction → main explanations/headings → definitions → worked example → important examination points supported by sources → related/prerequisite lessons → summary → source references → reviewed practice.

Target real unit: eight connected lessons, forty reviewed MCQs and two rights-cleared PDFs. Require a named human reviewer, factual/source checks, appropriate RPSC/RAS syllabus mapping, language/accessibility review and documented rights. The shipped synthetic reading-toolkit fixtures satisfy engineering coverage only; their fixture approval must never be copied as real editorial approval.

## Administrative accounts and navigation

Staff login/logout remains at `/admin/`. Superusers may manage staff accounts; learner reports, nonstaff account details and direct learner-model Admin/history URLs are closed. The previous Students navigation/report source is retained dormant; it is not a release toggle. The three primary sections are Topics, Content and Practice Questions, shown only for assigned permissions. Assign view/add/change permissions for the necessary Topics, blocks, resources, tags, aliases, relations, quizzes, questions and choices; no permission is granted automatically by migration. Superusers alone see advanced maintenance, extracted-page maintenance and staff-account management. PDF reviewers without extracted-page access can inspect the private source PDF; superusers can inspect extracted-page records. Saving a standalone Content block is draft-only. Tags are a controlled registry; normalized names and slugs must be unique. Slugs remain stable on tag renames. Published topic slug/parent stability remains the existing policy; relation/alias/question FKs remain stable regardless of title/slug edits.

## Module 4 — deterministic study planning

Local planner implemented with owned plans/tasks, selected published branches, Monday=0 days, daily capacity and approximate admin estimated_study_minutes per topic. Default 90 minutes is editable per plan; learning allocates 60/20/20% to learn/revise/practice, quick revision halves total (minimum 15), allocated 20/50/30%. Schedules split across chosen days, report exam feasibility and weekly/monthly subject totals. Edits/rescheduling preserve completed task IDs/timestamps and replace unfinished tasks; task completion is separate from marking a whole lesson completed. Migration 0011 is additive and not applied to existing data. Focused student backend: 30 passed. Production gate remains off by default.

## Student-platform content review batch — 23 October 2026

Prepare only a NEW destination with scripts/prepare_student_demo.py (README). The original SQLite, existing sample and demos must not be migrated/reset. New source fixture: backend/content/fixtures/student_lessons_v2.json. It contains 25 new lesson IDs, 10,929 note words, 125 MCQs and 500 choices, plus original sources and controlled tags. Seeded notes are editorial in_review, quizzes have no QuizReview approval and new aliases/relations stay draft. No human reviewer is invented. The private review-inventory.json records every syllabus path/reference/status and proposed relationship. Repeated unchanged seed runs are idempotent; altered notes cause refusal rather than overwrite.

| Actual root subject | Five existing lesson IDs / exact titles |
|---|---|
| History, Art, Culture, Literature, Tradition & Heritage of Rajasthan | 32 c. Palaces; 34 7. Various schools of paintings and handicrafts; 38 c. Folk Music & Instruments; 39 d. Folk Dances & Drama; 49 a. Fairs and Festivals |
| Ancient & Medieval Period | 56 a. Indus and Vedic Age; 66 d. Gupta; 69 g. Chola; 88 a. Bhakti; 89 b. Sufi Movement |
| Modern Period (from early 19th century to 1964) | 92 a. Intellectual awakening; 94 c. Western education; 99 b. Instituitions; 105 b. Institutional building during Nehruvian age; 106 c. Development of science and technology |
| World Geography | 109 a. Mountains; 110 b. Plateaus; 111 c. Plains; 113 2. Major Rivers; 114 3. Major Lakes |
| Geography of India | 125 a. Plateaus; 126 b. Plains; 127 c. Mountains; 130 10. Major Rivers of india; 131 11. Major Lakes of India |

The table preserves stored titles/spelling; stable slugs and full paths are in the private inventory. All new lessons are different from the prior 15 sample lessons. Primary MCQ locations use canonical lesson IDs; subject collections derive ancestry without copying questions. New practice remains unavailable publicly until human content publication and explicit quiz review.

Review references/facts/rights, format and MCQ explanations. Inspect private preview, approve suitable aliases/relationships, explicitly publish eligible ancestors/lesson and review the quiz. Run existing Suggest Connections/regenerate workflow and approve exact source evidence before active links appear. Withdrawal immediately suppresses public links/discovery. Draft proposals never masquerade as approved navigation. Existing old sample links/tag pages/practice remain engineering regression fixtures.

Topic estimated_study_minutes is an optional validated approximate total for learning/revision/practice. Planner defaults are labelled estimates. Student identity/planner/attempt records do not create a new Admin student-management scope; existing learner report restrictions remain.
