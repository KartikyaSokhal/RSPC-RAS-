# Changelog

All notable changes to the Prepal AI project will be documented in this file.

---

## [Unreleased] - 2026-06-29

### Added
* Comprehensive project documentation inside `/docs/` covering:
  * `PROJECT_ANALYSIS.md` (Current system state and technical debt analysis)
  * `IMPLEMENTATION_PLAN.md` (Phase planning and risk assessments)
  * `TASKS.md` (Checklist tracker for development milestones)
  * `ARCHITECTURE.md` (System components and RAG Mermaid flows)
  * `FEATURES.md` (Catalogue of active and planned modules)
  * `UI_UX_PLAN.md` (Visual design token system, skeletons, and layouts)
  * `AI_SYSTEM.md` (Isolated prompt structure and token management guidelines)
  * `API_DOCUMENTATION.md` (REST schema specifications)
  * `TESTING.md` (Unit test commands and manual QA lists)
  * `CONTRIBUTING.md` (Coding standards and Git guidelines)
  * `SKILLS.md` (Technology skills documentation)
* Created template `.env` configurations for environment security.
* Overwrote the root `README.md` file with a premium platform setup guide.

### Fixed
* Fixed server execution to bind on all host interfaces (`0.0.0.0`) so that both `localhost` and `127.0.0.1` resolve successfully on macOS systems.
* Recreated the virtual environment `.venv` with compatible Python versions and updated dependencies.
