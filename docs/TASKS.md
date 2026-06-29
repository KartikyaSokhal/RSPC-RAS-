# Prepal AI - Tasks Checklist

## Phase 1: Environment & Package Initialization
- [ ] Install python packages (`google-genai`, `python-dotenv`) in backend `.venv`.
- [ ] Configure `settings.py` to initialize `dotenv`.
- [ ] Verify server starts up properly without compile errors.

## Phase 2: Premium UI Redesign
- [ ] Build global CSS variables and colors (dark theme) in `src/App.css`.
- [ ] Redesign Header/Navbar and Footer in `src/pages/home.jsx`.
- [ ] Implement breadcrumbs and reading progress tracking in `src/pages/topicPage.jsx`.
- [ ] Add collapsible/accordion-style sidebar for syllabus hierarchy in `src/pages/topicPage.jsx`.

## Phase 3: AI Chatbot (Backend RAG Engine)
- [ ] Create `backend/content/ai_engine.py` wrapper to interact with Gemini API.
- [ ] Implement context generation function (recursively fetches text content from parent/child topics).
- [ ] Implement system prompt preset handlers (`explain_beginner`, `mnemonics`, etc.) in `ai_engine.py`.
- [ ] Write the `topic_chat` view function in `views.py` handling presets.
- [ ] Register URL pattern in `urls.py`.

## Phase 4: AI Chatbot (Frontend Integration)
- [ ] Build messaging state engine (`messages`, `input`, `loading`) in `topicPage.jsx`.
- [ ] Design interactive chatbot UI panel (styled bubbles, floating chat toggle, input actions).
- [ ] Implement a quick-action buttons grid (Beginner mode, Mnemonics, 5-Min Revision, etc.) above input.
- [ ] Integrate chatbot key triggers (Enter key submits message).

## Phase 5: Timed Quiz & MCQ Engine
- [ ] Create Quiz-related database models (`Quiz`, `Question`, `Choice`) in `models.py`.
- [ ] Create database migrations and apply them using `python manage.py migrate`.
- [ ] Write backend view functions to retrieve questions and submit scores.
- [ ] Create Frontend `quizPage.jsx` component.
- [ ] Set up timed test layout, auto-submit timer, and score board overlay.

## Phase 6: Bookmarks, Progress Tracking & Weakness Mapping
- [ ] Add `Bookmark`, `UserProgress`, and `QuizAttempt` models to track user metrics.
- [ ] Add Toggle Bookmark buttons to topic pages.
- [ ] Display list of Bookmarks on the Dashboard.
- [ ] Implement user weakness tracker endpoint `/api/profile/weaknesses/` providing personalized revision plans.
- [ ] Build UI Tab in AI chat sidebar displaying personalized Weakness analytics.
