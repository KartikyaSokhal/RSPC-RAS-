# Prepal AI - Features Catalog

This document details the functional features of the Prepal AI platform.

---

## 1. Syllabus Hierarchy Explorer
* **Purpose:** Allows students to browse the complete, layered RPSC/RAS syllabus using a clean, collapsible navigation tree.
* **Current Status:** Basic implementation in place; will be upgraded to a premium collapsible tree sidebar layout with smooth transitions.
* **Dependencies:** Backend APIs `GET /api/topics/` and `GET /api/topic/<slug>/`.
* **Future Improvements:** Add search filters, highlight active syllabus nodes, and display completion checkboxes directly on parent nodes.

---

## 2. AI Study Companion & Mentor
* **Purpose:** Acts as an interactive personal mentor right beside the reading content. In addition to answering user doubts, it offers dedicated one-click study buttons:
  * **Explain Like I'm a Beginner:** Simplifies complex RPSC exam details into layman's terms.
  * **Exam Importance:** Identifies weightage of the current topic (High/Medium/Low) for RPSC.
  * **Previous Year Questions (PYQ) Analysis:** Highlights trends and types of questions asked previously.
  * **Common Mistakes:** Lists typical traps students fall into for this topic.
  * **Memory Tricks:** Generates custom mnemonics to memorize key facts.
  * **Flashcards:** Generates Q&A pairs for active recall.
  * **5-minute Revision:** Delivers bulleted cheat sheets summarizing the main notes.
  * **Generate MCQs:** Instantly drafts 3 practice questions from the reading material.
  * **Examiner Mode:** The AI asks the user questions, evaluates their response, and guides them.
  * **Next Study Recommendations:** Identifies related topics to read next.
  * **Weakness Tracking & Revision:** Analyzes chatbot and quiz history to map weaknesses and design personalized study tracks.
* **Current Status:** Basic UI placeholder. To be implemented as an interactive side panel with quick-action trigger buttons.
* **Dependencies:** Python `google-genai` SDK, custom prompt pipelines, and database records of user progress/errors.
* **Future Improvements:** Voice-guided mentor mode and localized Hindi-English language support.

---

## 3. Timed Quiz & MCQ Testing Engine
* **Purpose:** Generates multiple-choice practice tests over syllabus segments. Features a countdown timer to simulate real exam pressure.
* **Current Status:** Not started. To be implemented in Phase 5.
* **Dependencies:** Database tables for Quizzes, Questions, and Choices; UI components with timer countdown state.
* **Future Improvements:** Adaptive difficulty (serving harder questions based on user's history), detailed explanations for wrong answers, and performance analytics.

---

## 4. Bookmarks & Revision Lists
* **Purpose:** Lets users save complex pages for fast revision access.
* **Current Status:** Not started. To be implemented in Phase 6.
* **Dependencies:** `Bookmark` model in database, user identification system, and bookmark status API endpoint.
* **Future Improvements:** Tagging bookmarks (e.g. "Hard", "Review Needed"), and exporting bookmarked text blocks as study guides.

---

## 5. Reading Progress Tracker
* **Purpose:** Visual indicators showing how much of a chapter a student has read.
* **Current Status:** Not started. To be implemented in Phase 6.
* **Dependencies:** Frontend scroll position monitoring, and saving completion states to the backend database.
* **Future Improvements:** Gamified achievements, study streak badges, and personalized study reminders.
