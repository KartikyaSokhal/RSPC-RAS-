# Prepal AI - Premium RPSC/RAS Prep Platform

Prepal AI is a modern, premium educational platform specifically designed for Rajasthan State Government Exam (RPSC/RAS) preparation. It features a hierarchical syllabus tree, study notes, a timed quiz testing engine, progress tracking, and an interactive context-aware AI chatbot powered by Google Gemini.

---

## Features
* **Hierarchical Syllabus Tree:** Drill down into subtopics to see specific study materials.
* **Premium Dark UI:** Designed with deep premium tones, glassmorphism cards, and responsive sidebars.
* **AI Chatbot (RAG):** Context-aware chatbot restricted to the selected chapter. It helps explain concepts, define words, create flashcards/mnemonics, and test your knowledge.
* **Timed Quiz Engine:** Timed tests generated over syllabus content with automatic scoring.
* **Bookmarks & Progress Tracker:** Save important chapters and track reading completion progress.

---

## Tech Stack
* **Frontend:** React, React Router, Axios, CSS (Vanilla Custom Design System)
* **Backend:** Django, Django REST Framework
* **AI Engine:** Google Gemini API (via `google-genai` SDK)
* **Database:** SQLite (default sqlite3 backend)

---

## Installation & Setup

### 1. Clone & Setup Workspace
Ensure your system has Python (>= 3.11) and Node.js (>= 18) installed.

### 2. Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # If requirements.txt is freeze-compiled
# Or install manually:
pip install django djangorestframework django-cors-headers python-dotenv google-genai
```

Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

Apply database migrations:
```bash
python manage.py migrate
```

### 3. Frontend Setup
```bash
cd ..
npm install
```

Create a `.env` file in the root `Prepal/` directory:
```env
VITE_API_BASE=http://127.0.0.1:8000/api
```

---

## Running Locally

### Start Django Backend
```bash
cd backend
source .venv/bin/activate
python manage.py runserver 127.0.0.1:8000
```

### Start Vite Frontend
```bash
cd ..
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

---

## Folder Structure
```
Prepal/
├── docs/               # Detailed architectural and design documentation
├── src/                # React Frontend code
│   ├── assets/
│   ├── pages/
│   │   ├── home.jsx    # Dashboard & Syllabus Catalog
│   │   ├── topicPage.jsx # Reading room & AI Chatbot
│   │   └── quizPage.jsx  # Timer Quiz testing interface
│   └── App.jsx
└── backend/            # Django Backend code
    ├── content/        # Content app (models, RAG views, serializers)
    └── core/           # Configuration settings
```

---

## API Overview
* `GET /api/topics/` - List all main syllabus segments.
* `GET /api/topic/<slug>/` - Retrieve full notes & subtopics for a syllabus segment.
* `POST /api/topic/<slug>/chat/` - Talk to the context-aware chatbot.
* `GET /api/topic/<slug>/quiz/` - Retrieve Quiz questions for the chapter.
* `POST /api/topic/<slug>/quiz/submit/` - Submit answers and receive scores.
