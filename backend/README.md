# Prepal Django backend

The active backend is Django/DRF + SQLite + Django Admin. Legacy `src/` Express/Mongo is preserved but disabled; do not run `npm start` or use its dependencies for deployment.

From the application root follow [the safe demo setup](../README.md). Run `backend/.venv/bin/python backend/manage.py runserver 127.0.0.1:8000 --settings=core.demo_settings` for synthetic fixtures/mock AI. Credentials remain private under `.local/demo`. Normal settings use `.env` only when deliberately configured; migration of the existing real database still needs approval.

Tests: from backend, `.venv/bin/python run_tests.py`. Runtime/dev locks are hash pinned. Admin/PDF workflow: [ADMIN_WORKFLOW](../docs/ADMIN_WORKFLOW.md). Deployment and backups: [DEPLOYMENT](../docs/DEPLOYMENT.md). Actual results: [verification](../docs/evidence/MVP_IMPLEMENTATION_VERIFICATION.md).
