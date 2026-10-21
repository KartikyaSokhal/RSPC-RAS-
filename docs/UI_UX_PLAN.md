> Current authority: the Phase 4A conversation map and approved Phase 4B frontend brief. Targeted changes reuse existing components/tokens. Student accounts/dashboard remain disabled; real cutover, paid AI and Phase 5 require separate approval. Actual commands/screenshots/results are in [TESTING](TESTING.md).


# Current UI/UX Design System — Phase 4B

The existing light/dark token system, Rajasthan SVG map and React components are retained. Phase 4B simplifies header/homepage/footer navigation, numbers the shared hierarchy and consolidates the reader Tutor. No complete redesign or student dashboard is introduced.

## 1. Single Coherent Brand Identity
The multi-palette selector was replaced with a focused, prestigious academic theme tailored for RPSC RAS candidates:

### Light Mode (Default)
- **Backgrounds**: Soft white `#f8fafc` and warm-neutral surfaces `#ffffff`, `#f1f5f9`.
- **Primary Text**: Deep navy `#0f172a`.
- **Muted Text**: Slate `#475569`.
- **Accents**: Muted royal-blue `#1e40af` (hover `#1e3a8a`).
- **Borders & Dividers**: Subtle line borders `#e2e8f0`.
- **Cards**: Clean, elevated cards with subtle shadow (`0 4px 16px -2px rgba(15, 23, 42, 0.07)`).

### Dark Mode
- **Surfaces**: Deep charcoal and navy `#111827`, `#1e293b`, with canvas `#0b0f17`.
- **Primary Text**: Soft crisp off-white `#f8fafc`.
- **Muted Text**: Soft slate `#cbd5e1`.
- **Accents**: Restrained sky-blue `#60a5fa` (hover `#93c5fd`).
- **Contrast evidence**: current automated accessibility scans report zero violations for the tested page/theme states; no AAA certification or manual assistive-technology coverage is claimed.

### Theme Toggle
- Minimalist sun/moon icon toggle button in the navbar (`button.theme-toggle-btn`).
- Replaces the previous large pill-shaped dropdown.
- Preferences saved in `localStorage['prepal-theme']` with system preference auto-detection.

## 2. Simplified Navigation
- Header: Prepal logo left, empty center, prominent Search link to the existing `/search` page and theme toggle right. The same two controls are visible on mobile without a redundant drawer.
- No header Syllabus/About/auth links. Their routes remain; footer retains Syllabus/Search/Help & Privacy.
- Footer keeps Prepal Academic Syllabus branding, dynamic subject/curriculum-topic counts and noninteractive future social space. Loading/error states never invent counts.

## 3. Homepage with Rajasthan Visual Identity
- Reuse RajasthanMap.jsx without changing its SVG geometry/aspect ratio. Reduce hero padding/gap and map maximum width, with smaller tablet/mobile sizing.
- Retain Explore Syllabus; remove Search Topics hero action. Assistant copy only describes help understanding available lesson sources and checking citations.
- Remove homepage explorer search/status controls. API-derived subject buttons scroll/focus root sections without filtering or changing routes.

## 4. Dynamic Counts and Stable Hierarchy
- AppShell shares one current hierarchy resource with Home/SyllabusPage/TopicPage. Homepage shows only Total Curriculum Topics and Core Subjects; footer uses the same counts. No hardcoded source/demo fallbacks for these displays.
- Root numbers follow original API order; children use dotted numbers; deeper levels restart letters within each parent. Filtered reader/full-syllabus trees preserve original positions and slugs.
- Expand All opens every branch; Collapse All retains root labels; individual native summary toggles work after both actions. No Default View control.
- The standalone `/syllabus` page retains its preexisting search/status controls and copy, outside the homepage simplification.

## 5. Content-first Topic Reader
- Preserve Phase 3 safe approved hyperlinks, revalidated contextual popups, tags/related content and stateless practice.
- One bottom-right Tutor launcher; remove toolbar/mobile Tutor controls. Panel opens only on request/passage action, stays within viewport bounds, and supports Close/Escape with focus restoration without scrolling. It is nonmodal and reading remains accessible.
- Keep disabled learner controls; dashboard/account routes still show the release-boundary notice. No bookmark/progress/saved-attempt state is activated.

## 6. Motion & Animation System
- **Microinteractions**: 140ms with `cubic-bezier(0.16, 1, 0.3, 1)` for snappy button hovers and badge highlights.
- **Transitions**: 220ms for existing popup and card entrance effects.
- **Reduced Motion**: Full support for `@media (prefers-reduced-motion: reduce)` which zeroes animation durations.
