# Prepal AI - Project Analysis

## 1. Existing Architecture
The current project is a decoupled client-server web application comprised of:
- **Frontend (Client):** Built with React and Vite, using Axios for HTTP requests and React Router DOM for routing. It runs on `http://localhost:5173`.
- **Backend (Server):** Built with Django and Django REST Framework (DRF), running on `http://127.0.0.1:8000`. It utilizes Django's default ORM and SQLite (`db.sqlite3`) as the storage engine.
- **Content Management:** Uses Django Admin Panel at `/admin/` to manage syllabus topics and content.

## 2. Folder Structure
```
Prepal/
├── README.md
├── eslint.config.js
├── index.html
├── package-lock.json
├── package.json
├── vite.config.js
├── public/
├── src/
│   ├── App.css
│   ├── App.jsx
│   ├── main.jsx
│   ├── assets/
│   └── pages/
│       ├── home.jsx
│       └── topicPage.jsx
└── backend/
    ├── manage.py
    ├── db.sqlite3
    ├── package.json
    ├── package-lock.json
    ├── django.log
    ├── content/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── views.py
    ├── core/
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── .venv/
```

## 3. Current APIs
- **GET** `/api/topics/`
  * Lists all root-level topics (topics where `parent` is null) with titles, slugs, and a `has_children` boolean indicator.
- **GET** `/api/topic/<slug:slug>/`
  * Returns detailed topic information including its title, slug, list of subtopics (`children`), and its ordered `blocks` (content blocks of types heading, text, image, or pdf).

## 4. Current Frontend Pages
- **Home Page (`home.jsx`):** Renders the RPSC Pre Syllabus hierarchical list. Supports lazy-loading of subtopic nodes upon expansion (drill-down).
- **Topic Page (`topicPage.jsx`):** Renders the title and list of ordered content blocks for a specific syllabus topic. Contains a static mockup of an "Ask AI" sidebar widget.

## 5. Existing Models & Database Relations
- **Topic:**
  * `title` (CharField, max_length=255)
  * `slug` (SlugField, unique=True)
  * `parent` (ForeignKey pointing to self, null=True, blank=True, related_name="children", on_delete=models.CASCADE)
  * `order` (PositiveIntegerField, default=0)
  * Represents the syllabus hierarchy.
- **ContentBlock:**
  * `topic` (ForeignKey to Topic, related_name="blocks", on_delete=models.CASCADE)
  * `block_type` (CharField with choices: heading, text, pdf, image)
  * `content` (TextField, blank=True)
  * `file` (FileField uploading to `content/`, blank=True, null=True)
  * `order` (PositiveIntegerField)
  * Holds the granular content for each topic.

## 6. Authentication Flow
* Currently, the app is open-access with no active user registration or authentication for viewing syllabus content.
* Django Admin utilizes standard Django session-based authentication for superusers.

## 7. Admin Workflow
* Django Admin serves as the content editor where administrators can create, edit, or delete `Topic` objects and upload `ContentBlock`s (notes, heading structure, PDFs, images).

## 8. Technical Debt & Improvement Opportunities
- **Technical Debt:**
  * Hardcoded API endpoints (`http://127.0.0.1:8000/api`) in React pages rather than using environment variables (`import.meta.env.VITE_API_BASE`).
  * Lack of unit/integration testing on both frontend and backend.
  * Static UI design styling using a monolithic `App.css` rather than a modular, component-specific CSS system.
- **Improvement Opportunities:**
  * Re-architecting the frontend layout with a premium visual design, dark mode, responsive sidebars, and skeletons.
  * Creating a dedicated user profile, bookmarks, and revision list state in the database.
  * Implementing a RAG (Retrieval-Augmented Generation) API in Python to connect the existing syllabus contents to Google Gemini.
  * Introducing a Quiz model and API system to generate timed tests over syllabus topics.

## 9. Risk Analysis
- **Gemini API Usage:** High user traffic can quickly exhaust free-tier token allowances. Mitigation: Backend rate-limiting and local caching of AI responses.
- **Context Size:** Large syllabus chapters can exceed context limits or increase latency. Mitigation: Build a chunked token-optimized context payload containing only headings and text blocks relevant to the requested topic.
