# Prepal AI - Contributing Guidelines

Welcome to the Prepal AI development team! To maintain high code quality and consistency, please adhere to these guidelines.

---

## 1. Coding Standards

### Python & Django (Backend)
* **Style:** Adhere strictly to **PEP 8**. Use double quotes for strings where possible.
* **Typing:** Use Python type hinting where applicable (e.g. `def my_func(arg: str) -> bool:`).
* **Django Models:** Always specify a verbose name, define `__str__` methods, and add appropriate comments.
* **Separation of Concerns:** Keep views simple. Write heavy business logic (e.g. AI queries, RAG processing) in standalone services/managers like `ai_engine.py`.

### JavaScript & React (Frontend)
* **Naming:** Use PascalCase for React component files (e.g. `QuizPage.jsx`) and camelCase for functions and variables.
* **State Management:** Place states near where they are used. Avoid global state unless absolutely necessary.
* **CSS Rules:** Use vanilla CSS variables. Put general rules in `App.css` and use specific comments. Do not inline styles unless dynamic (e.g. `style={{ marginLeft: level * 16 }}`).

---

## 2. Git & Commit Strategy

* **Branching Model:**
  * Develop features in separate branches prefixed by type: `feat/quiz-engine`, `fix/api-cors`, `docs/refactor`.
* **Commit Messages:**
  * Keep messages structured and concise. Prefer the conventional commits format:
    * `feat(chatbot): connect react input to backend rag api`
    * `fix(cors): allow local frontend dev server access`
    * `docs(readme): update setup and execution commands`
