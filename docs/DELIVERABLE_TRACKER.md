# Deliverable Tracker

| Deliverable | Required output | File or evidence location | Status | Verification method | Remaining work |
|---|---|---|---|---|---|
| D1 | Proposal and requirements | `docs/PROJECT_SYNOPSIS.md` | Complete | Read against requirements | None |
| D2 | Schema, models, migration, ER, dictionary, seed | `schema.sql`, `app/models.py`, `migrations/`, `docs/ER_DIAGRAM.md`, `docs/DATA_DICTIONARY.md`, `app/services/seed.py` | Complete | SQLite init/seed completed; model/schema inspection | Apply and verify on a real MySQL server |
| D3 | Flask backend and API docs | `app/`, `docs/API_DOCUMENTATION.md` | Complete for SQLite demo | 6 pytest cases and local health endpoint | Real MySQL connectivity verification |
| D4 | Data analysis methodology | `app/services/analytics.py`, `docs/ANALYSIS_METHODOLOGY.md` | Complete | Runtime sample summaries and tests | None |
| D5 | Four live charts and interpretation | `artifacts/charts/demo_*.png`, `docs/CHARTS_AND_INTERPRETATION.md` | Complete | Files generated from seeded records and visually inspected | Browser screenshots not captured |
| D6 | Tests and report | `tests/`, `docs/TEST_REPORT.md` | Complete with stated scope | `pytest -q`: 8 passed | MySQL/restart/browser tests unverified |
| D7 | README and technical documents | `README.md`, `docs/*.md` | Complete | File review and cross-links | Update if code changes |
| D8 | Demonstration material | `docs/DEMONSTRATION_PLAN.md`, `deliverables/Home_Budget_Project_Presentation_v4.pptx` | Complete | 10-slide deck exported, structurally validated, and visually inspected | None |

## Final verification

- [x] Complete source code, SQL schema, seed script, README, and final report exist.
- [x] Local SQLite demo initialized and demo data loaded without duplication.
- [x] Dashboard/API workflow, formulas, charts, CSV safety, and automated tests have executable evidence.
- [x] Charts are database-derived and no bank/payment data is used.
- [x] Documentation identifies manual-entry boundaries and actual verification limitations.
- [x] Demonstration presentation contains project overview, architecture, database design, analytics, visualizations, test evidence, limitations, and conclusion.
- [ ] Configure a real MySQL server with `DATABASE_URL`, run initialization, and repeat the health/API workflow.
- [ ] Capture browser screenshots if the submission requires interface screenshots.

## Deployment note

The repository is Vercel-ready through `api/index.py` and `vercel.json`. Deployment has not been started because no Vercel login or hosted MySQL credentials are configured in this workspace. A public production URL must use MySQL; local SQLite is demonstration-only and not durable on serverless infrastructure.
