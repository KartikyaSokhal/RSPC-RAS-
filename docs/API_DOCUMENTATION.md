# Prepal AI - API Reference Manual

This file lists the specifications for all REST endpoints exposed by the Django Backend.

---

## 1. Syllabus Catalog

### List Root Topics
* **Endpoint:** `/api/topics/`
* **Method:** `GET`
* **Authentication:** None
* **Response (200 OK):**
  ```json
  [
    {
      "title": "History, Art & Culture of Rajasthan",
      "slug": "history-art-culture-heritage",
      "has_children": true
    }
  ]
  ```

### Topic Detail & Reading Content
* **Endpoint:** `/api/topic/<slug:slug>/`
* **Method:** `GET`
* **Authentication:** None
* **Response (200 OK):**
  ```json
  {
    "title": "Ancient & Medieval Period",
    "slug": "ancient-medieval-period",
    "children": [
      {
        "title": "Pre-historical Sites",
        "slug": "pre-historical-sites",
        "has_children": false
      }
    ],
    "blocks": [
      {
        "block_type": "heading",
        "content": "Pre-historic Archaeological Sites",
        "file": null,
        "order": 1
      },
      {
        "block_type": "text",
        "content": "Detailed text notes about sites like Bagore, Tilwara...",
        "file": null,
        "order": 2
      }
    ]
  }
  ```

---

## 2. AI Chatbot

### Ask AI Doubts (RAG)
* **Endpoint:** `/api/topic/<slug:slug>/chat/`
* **Method:** `POST`
* **Authentication:** None (Optional session token)
* **Request Payload:**
  ```json
  {
    "message": "Where is the site of Bagore located?"
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "response": "Bagore is located on the Kothari river in Bhilwara district..."
  }
  ```
* **Error Responses:**
  * **400 Bad Request:** `{ "error": "Message field is required." }`
  * **503 Service Unavailable:** `{ "error": "Gemini API key is not configured or service is down." }`

---

## 3. MCQ Quiz Engine

### Fetch Topic Quiz
* **Endpoint:** `/api/topic/<slug:slug>/quiz/`
* **Method:** `GET`
* **Authentication:** None
* **Response (200 OK):**
  ```json
  {
    "quiz_title": "Ancient Period MCQ Challenge",
    "time_limit_seconds": 600,
    "questions": [
      {
        "id": 15,
        "question_text": "Which river flows near the archaeological site of Bagore?",
        "choices": [
          {"id": 41, "text": "Banaili"},
          {"id": 42, "text": "Kothari"},
          {"id": 43, "text": "Luni"}
        ]
      }
    ]
  }
  ```

### Submit Quiz Responses
* **Endpoint:** `/api/topic/<slug:slug>/quiz/submit/`
* **Method:** `POST`
* **Authentication:** None
* **Request Payload:**
  ```json
  {
    "answers": {
      "15": 42
    }
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "score": 1,
    "total": 1,
    "percentage": 100.0,
    "results": [
      {
        "question_id": 15,
        "user_answer": 42,
        "correct_answer": 42,
        "is_correct": true
      }
    ]
  }
  ```
