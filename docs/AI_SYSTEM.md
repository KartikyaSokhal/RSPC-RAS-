# Prepal AI - AI System Design (RAG)

This document details the retrieval and response generation pipeline for Prepal's RPSC Chatbot.

---

## 1. Content Storing & Extraction
* All RPSC syllabus chapters are stored natively in the SQLITE database via the `Topic` and `ContentBlock` models.
* To prepare the search context, the backend queries the database for the active topic. If it has parent topics, we collect parent names. If it has child topics, we list those subheadings.
* The content blocks are filtered to pull out `heading` and `text` block content types, ignoring binary fields (like image files or PDFs) to preserve prompt size.

---

## 2. Context-Aware Prompt Design
* We formulate a system prompt constraining the assistant to act as a highly specialized Rajasthan State Exam prep coach.
* **Hierarchy Aware Context Builder:**
  If a user requests information, we provide the context showing their position in the syllabus layout:
  ```
  Topic Hierarchy: {Parent Topic} > {Active Topic} > {Child Topics}
  Active Notes:
  {ContentBlock text contents concatenated...}
  ```
* **AI Mentor Presets & System Commands:**
  We add structured commands to the endpoint `POST /api/topic/<slug>/chat/` with a `"preset"` parameter (e.g. `{"preset": "mnemonics"}`):
  * **`explain_beginner`:** "Rewrite the provided topic notes in extremely simple terms suitable for a absolute beginner. Use real-life analogies."
  * **`exam_importance`:** "Analyze the notes and rank the RPSC exam importance as High, Medium, or Low. Explain why in 2 sentences based on past paper trends."
  * **`pyq_analysis`:** "List typical questions asked in RPSC RAS prelims/mains from this topic and detail how to address them."
  * **`common_mistakes`:** "Outline 3 common pitfalls or factual confusion students face in this topic (e.g. mixing up dynasties or geographic boundaries)."
  * **`mnemonics`:** "Create catchy, easy-to-remember mnemonics (Hindi/English mixing allowed) for the main dates, names, or lists in the context."
  * **`flashcards`:** "Format exactly 5 question-and-answer flashcard units from this material."
  * **`revision`:** "Produce a 5-minute bulleted summaries list focusing on core high-yielding facts."
  * **`generate_mcqs`:** "Generate 3 high-quality RPSC standard MCQs with options A-D and a hidden explanation field."
  * **`examiner_mode`:** "Ask me one single challenging question based on the topic notes. Wait for my response before asking follow-up questions."
  * **`next_topics`:** "Based on this syllabus section, recommend the next logical 2 topics to read next and explain the connection."
* **System Prompt Constraints:**
  1. *Context boundaries:* "You are a professional tutor for RPSC exams. Rely first on the provided context. If the answer is not in the context, use your general knowledge, but flag it to the user. Never state facts that contradict historical or geographical truths."
  2. *Tone:* Concise, structured, preferring bullet points and tabular formats.
  3. *Cross-references:* "If the context mentions subtopics (e.g. {Subtopic A}), remind the user that further details can be found under that specific sub-chapter."

---

## 3. Caching & Token Optimization
* **Max Context Trim:** Keep context blocks capped at 6,000 tokens (approx. 4,500 words). If a topic is abnormally large, we truncate oldest content blocks or select blocks matching search keywords.
* **Isolating Client Operations:** All Gemini client connections are isolated in `backend/content/ai_engine.py`. The controller interacts with a high-level `ask_gemini(context, question, history)` function. If we swap Gemini for another model or managed RAG, the API and frontend remain unchanged.

---

## 4. Hallucination Prevention & Error Handling
* **Out-of-Syllabus questions:** If a user asks "Who won the 2024 NBA Finals?", the bot replies: *"I am optimized to answer doubts related to the syllabus of {Active Topic}. That question is outside the scope of our RPSC preparation."*
* **API Fault Tolerance:** If the Gemini API fails, returns rate limits (error 429), or goes offline, the backend catches the exception and returns a friendly local fallback error: *"I'm having trouble connecting to my AI brain. Please try again in a few seconds."*
