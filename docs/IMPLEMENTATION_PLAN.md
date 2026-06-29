# Prepal AI - Implementation Plan

We will transform Prepal into a premium RPSC exam preparation platform in structured, testable phases.

---

## Phase 1: Setup & Core Infrastructure
* **Goal:** Configure environment settings, load secret keys, and install required libraries.
* **Files Affected:**
  * `backend/core/settings.py` (add dotenv loader, configure static paths)
  * `backend/package.json` & `backend/.venv` (pip install `google-genai` and `python-dotenv`)
  * `Prepal/.env` (add environment variable `VITE_API_BASE`)
* **APIs Required:** None.
* **Database Changes:** None.
* **Risks:** Broken package installations.
* **Testing:** Run `./.venv/bin/python manage.py check` to ensure Django boots correctly.

---

## Phase 2: Premium UI/UX Redesign
* **Goal:** Build the design system, global layout, responsive navbar, collapsible sidebar with topic hierarchy, and beautiful typography.
* **Files Affected:**
  * `src/App.css` (redesign modern color scheme, typography, and styling variables)
  * `src/pages/home.jsx` (add hero section, syllabus catalog card list, search filters)
  * `src/pages/topicPage.jsx` (integrate breadcrumbs, collapsible layout, reading progress bar)
* **APIs Required:** Existing `GET /api/topics/` and `GET /api/topic/<slug>/`.
* **Database Changes:** None.
* **Risks:** Layout breaks on smaller screen viewports.
* **Testing:** Manual responsiveness audit in the browser.

---

## Phase 3: AI Chatbot (Backend RAG Engine)
* **Goal:** Build a robust, isolated RAG system that pulls syllabus text from Django's database and forwards it as context to Gemini. Extend the controller to handle mentor presets.
* **Files Affected:**
  * `backend/content/ai_engine.py` [NEW] (encapsulates RAG prompts, system constraints, presets like mnemonics, beginner mode, and MCQ generator, using Gemini SDK)
  * `backend/content/views.py` (add `topic_chat` endpoint accepting optional `"preset"` query parameter)
  * `backend/content/urls.py` (map `/api/topic/<slug>/chat/`)
* **APIs Required:**
  * **POST** `/api/topic/<slug>/chat/` (Accepts payload `{ "message": "...", "preset": "explain_beginner" | "mnemonics" | "flashcards" | "revision" | "generate_mcqs" | "examiner_mode" | "exam_importance" | "pyq_analysis" | "common_mistakes" | "next_topics" }`)
* **Database Changes:** None.
* **Risks:** Rate limits, token limits, context formatting issues.
* **Testing:** Curl test the API endpoint with various preset payloads. Verify response formats.

---

## Phase 4: AI Chatbot (Frontend Integration)
* **Goal:** Hook up the `.ai-chat` sidebar to the backend API with message histories, preset buttons, loading states, and examiner mode.
* **Files Affected:**
  * `src/pages/topicPage.jsx` (update chatbot container with active state, message list, quick-action action buttons grid, and axios calls forwarding the preset parameter)
* **APIs Required:**
  * **POST** `/api/topic/<slug>/chat/`
* **Database Changes:** None.
* **Risks:** Slow response times from Gemini causing UI lag.
* **Testing:** Browser subagent manual conversation and action click tests.

---

## Phase 5: Timed Quiz & MCQ Engine
* **Goal:** Implement quiz capabilities allowing users to take timed quizzes on the syllabus.
* **Files Affected:**
  * `backend/content/models.py` (add Quiz, Question, and Choice models)
  * `backend/content/views.py` (endpoints to fetch quiz, submit responses, calculate scores)
  * `backend/content/urls.py` (routes for quizzes)
  * `src/App.jsx` (add `/quiz/:slug` route)
  * `src/pages/quizPage.jsx` [NEW] (quiz interface, timer, scorecard display)
* **APIs Required:**
  * **GET** `/api/topic/<slug>/quiz/` (retrieves questions)
  * **POST** `/api/topic/<slug>/quiz/submit/` (scores the exam)
* **Database Changes:**
  * Add tables `content_quiz`, `content_question`, `content_choice`.
* **Risks:** Database migrations.
* **Testing:** Django unit tests for scoring logic.

---

## Phase 6: Profile & Bookmarks (Educational Polish & Weakness Mapping)
* **Goal:** Add bookmarks, recently viewed, reading progress indicators, and AI weakness analysis tracking.
* **Files Affected:**
  * `backend/content/models.py` (add Bookmark, Progress, and QuizAttempt models to log incorrect questions)
  * `backend/content/views.py` (endpoints for bookmarking, progress saving, and AI weakness summary analysis)
  * `src/pages/topicPage.jsx` (add bookmark toggle, update reading progress, and add a weakness analysis dashboard tab)
  * `src/pages/home.jsx` (display progress markers and bookmarked nodes)
* **APIs Required:**
  * **POST** `/api/topic/<slug>/bookmark/`
  * **POST** `/api/topic/<slug>/progress/`
  * **GET** `/api/profile/weaknesses/` (gathers incorrect attempts and generates a personalized revision plan)
* **Database Changes:**
  * Add tables `content_bookmark`, `content_progress`, `content_quizattempt`.
* **Testing:** Validate progress save/restore states and correct weakness aggregation.
