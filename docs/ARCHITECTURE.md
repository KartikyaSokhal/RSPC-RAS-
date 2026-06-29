# Prepal AI - Architecture Reference

This document explains the architecture, data flow, and RAG integration for the Prepal AI platform.

---

## 1. System Overview

Prepal AI utilizes a decoupled client-server architecture. The frontend application fetches rendering data and interacts with services using REST endpoints.

```mermaid
graph TD
  A[React Frontend] -->|HTTP Requests| B[Django REST Framework]
  B -->|Queries| C[(SQLite DB)]
  B -->|AI Context + User Query| D[Google Gemini API]
```

---

## 2. Frontend Architecture
* **State Management:** Simple reactive React hooks (`useState`, `useEffect`).
* **Routing:** `react-router-dom` handles page paths (`/` for home, `/topic/:slug` for reading room, `/quiz/:slug` for testing).
* **Styling:** Modular CSS styled with modern custom properties (colors, typography, grid/flex layouts).

---

## 3. Backend Architecture
* **Routing & Controllers:** Django REST framework handles requests, executes custom RAG or quiz logic, and returns formatted JSON data.
* **Content Service:** Django Admin manages syllabus uploads. DB queries are highly optimized to fetch syllabus hierarchies efficiently.
* **AI Service (RAG):** The AI module is completely isolated in `ai_engine.py`. This ensures we can migrate to vector databases (like Vertex AI Vector Search) without changing view endpoints or API schemas.

---

## 4. RAG Chatbot Data Flow

When a user submits a question on a topic page, the RAG engine performs the following tasks:

```mermaid
sequenceDiagram
  autonumber
  User->>Frontend: Type question & click Send
  Frontend->>Backend: POST /api/topic/{slug}/chat/ (message)
  Backend->>Database: Query Topic & ContentBlocks
  Database-->>Backend: Return text content (notes)
  Backend->>Backend: Build context template & isolate prompt
  Backend->>Gemini API: generate_content(context + query)
  Gemini API-->>Backend: Return text response
  Backend-->>Frontend: Return JSON { response: ... }
  Frontend-->>User: Render bot bubble on screen
```

---

## 5. Timed Quiz Flow

```mermaid
sequenceDiagram
  autonumber
  User->>Frontend: Click "Start Timed Quiz"
  Frontend->>Backend: GET /api/topic/{slug}/quiz/
  Backend->>Database: Get Questions & Choices
  Database-->>Backend: Return Quiz Data
  Backend-->>Frontend: Return JSON Quiz details
  Frontend->>Frontend: Start Timer
  User->>Frontend: Answer MCQs
  Frontend->>Backend: POST /api/topic/{slug}/quiz/submit/ (answers)
  Backend->>Backend: Calculate score and performance metrics
  Backend-->>Frontend: Return JSON { score: X, total: Y, correct_answers: [...] }
  Frontend-->>User: Display scorecard
```

---

## 6. Future Scalability
* **Vector DB Integration:** If notes expand to thousands of pages, the query engine can easily switch to pgvector or Vertex AI, using embeddings to retrieve the top 3-5 most relevant chunks.
* **Model Upgrades:** The isolated `ai_engine.py` allows upgrading models (e.g. from `gemini-2.5-flash` to advanced reasoning models) with a single string replacement.
* **Caching Layer:** Introduce Redis to cache RAG contexts and repeat questions, reducing latency and api costs.
