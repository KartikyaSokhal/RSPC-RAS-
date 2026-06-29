# Prepal AI - Testing & Quality Assurance Plan

This document outlines the testing strategies and validation procedures to be followed throughout development.

---

## 1. Automated Unit Testing

### Backend Tests (Django)
Create tests inside `backend/content/tests.py` covering:
* **Topic Hierarchy Serialization:** Test that `GET /api/topics/` loads parent/child nodes properly.
* **Quiz Grading Logic:** Unit test that the submit endpoint calculates marks correctly.
* **Command:** Run `python manage.py test` to execute tests.

### Frontend Tests (React)
Using React Testing Library / Jest to test:
* **Message Rendering:** Chatbot successfully displays a bot message upon receiving a prop.
* **Timer Countdown:** Test that the quiz timer decreases every second and auto-submits when reaching zero.

---

## 2. API Integration & RAG Validation

* **Mock AI Client:** Write unit tests for `ai_engine.py` using unit mocks so we do not deplete real Gemini API keys during routine test runs.
* **Validation Script:** Run a script to hit `/api/topic/history-art-culture-heritage/chat/` and check if the returned string matches our expected schema format (contains "response").

---

## 3. UI/UX Verification Checklist (Manual)

Perform manual verification across these viewports:
- [ ] **Desktop (1440px+):** Sidebar tree navigation remains sticky. Chat panel sits fixed on the right without overlapping notes.
- [ ] **Mobile (375px - 768px):** Chat sidebar turns into a clean slide-up sheet. Sandwich menu toggles Left Sidebar list.

---

## 4. Performance Audit
* **Vitals Target:** Largest Contentful Paint (LCP) under 2.5s.
* **Code Splitting:** Verify that routing between `/` and `/topic/:slug` utilizes React Lazy loading.
* **Query count:** Ensure database query profiling (`django-debug-toolbar` or logging SQL statements) verifies that detail queries perform no more than 3 SELECT statements to resolve child and content block arrays.
