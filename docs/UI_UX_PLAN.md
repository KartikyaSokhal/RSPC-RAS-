# Prepal AI - UI/UX Design System & Layout Plan

This document outlines the design patterns, interactive elements, accessibility rules, and layouts for Prepal AI.

---

## 1. Visual Theme & Palette

We employ a modern, professional, dark-mode-first aesthetic reminiscent of premium streaming and educational portals.

* **Primary Dark Background:** `#0B0F19` (rich deep indigo-navy)
* **Secondary Card Background:** `#161E2E` (slate blue card body)
* **Accent Color:** `#3B82F6` (vibrant cobalt blue)
* **Success/Progress Color:** `#10B981` (emerald green)
* **Text (Primary):** `#F3F4F6` (near white)
* **Text (Secondary):** `#9CA3AF` (cool grey)
* **Borders/Dividers:** `#243048`

---

## 2. Layout Structure

### Reading Room Page Layout
```
+-------------------------------------------------------------+
|  [Logo] Prepal AI                 [Bookmarks]  [Profile]    |  <-- Navbar
+-------------------------------------------------------------+
|  Breadcrumbs: Topics > History > Ancient Sites               |
+---------------------+-----------------------+---------------+
|                     |                       |               |
|  Topic Tree         |  Reading Material     |  Ask AI       |
|  Sidebar (Left)     |  Content Pane         |  Chat Box     |
|                     |  (Center)             |  (Right)      |
|  - Collapsible      |                       |               |
|  - Active highlights|  - Notes              |  - Bubbles    |
|  - Progress check   |  - Images             |  - Suggestions|
|                     |  - PDF Viewer         |  - Flashcards |
|                     |  - timed quiz btn     |               |
+---------------------+-----------------------+---------------+
|  Progress Bar [============ 65% ============]               |  <-- Footer Tracker
+-------------------------------------------------------------+
```

---

## 3. Core UI Details

* **Sidebar Tree Navigation:** Left sidebar displays syllabus nodes. Expanding parent nodes shows sub-branches with smooth transitions. Clicking a leaf node routes the reader to its material.
* **Sticky Header Navbar:** Transparent blurred glass header containing logo, search field, bookmark shortcuts, and avatar menu.
* **Reading Progress Tracker:** A slim green linear progress bar fixed to the top/bottom of the reading panel that increases as the user scrolls down the chapter.
* **AI Chat Sidebar Panel (AI Study Companion):** Floating side drawer on desktop; slides in from bottom on mobile devices.
  * **Quick Action Button Deck:** Displays a grid/carousel of icon shortcuts (e.g. 🎓 *Beginner Explain*, 🧠 *Mnemonics*, ⚡ *5-Min Revision*, 📝 *Generate MCQs*, 🎯 *Examiner Mode*, 🔍 *PYQ Analysis*) positioned directly above the input box.
  * **Chat Bubbles:** Uses distinct background bubbles for user (vibrant blue/indigo with rounded corners) vs chatbot (dark slate/grey with support for Markdown headings, bold texts, and bullet lists).
  * **Status & Loading:** Shows typing indicators and skeleton ripples while the RAG engine queries Gemini.
  * **Toggle Tabs:** Tab buttons at the top of the AI drawer to switch between "Doubt Chat" and "Personalized Revision & Weakness Dashboard".
* **Skeleton Loaders:** Prevents layout shifts by showing gradient animated boxes while topics or quiz cards are downloading.
* **Animations:** Subtle transition timings (150ms-250ms) for accordion toggles, button hovers, and dialog modals.

---

## 4. Accessibility & Responsiveness
* **A11y:** High-contrast text, focus rings on keyboard navigations, and clean semantic heading structures (`h1`, `h2`, `h3`, `p`, etc.).
* **Responsive Layouts:**
  * **Desktop:** Three-column view (Sidebar, Content, Chat).
  * **Tablet:** Two-column view (Sidebar toggles dynamically; Content & Chat sidebar are side-by-side).
  * **Mobile:** Single-column view (Content occupies full screen, with fixed floating action buttons to toggle the topic menu or open the slide-up chat module).
