# Home Budget Expense Tracker and Analysis System

A Flask application for manually recording household income and expenses, setting category budgets, reviewing monthly savings, generating charts, and exporting reports. It is an educational prototype for a trusted local environment, not a banking product or source of financial advice.

## Features

- Income and expense CRUD with decimal currency values, filters, search, sorting, pagination API, and validation.
- Safe category management, idempotent default categories, and protected deletion for referenced categories.
- Monthly category budgets with utilization, variance, remaining balance, approaching-limit, overspend, and unbudgeted-spend states.
- Pandas and NumPy summaries, trend analysis, category contributions, four Matplotlib charts, JSON APIs, and CSV exports protected against spreadsheet formula injection.
- MySQL SQLAlchemy configuration, an initial Alembic migration, `schema.sql`, optional SQLite demo mode, pytest coverage, and academic documentation.

## Stack

Python 3.12, Flask, SQLAlchemy, Flask-Migrate, PyMySQL, Pandas, NumPy, Matplotlib, Jinja2, HTML/CSS, and pytest.

## Setup on Windows PowerShell

```powershell
cd "C:\Users\gdhan\OneDrive\Music\Documents\ChatGPT\home expenses"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
Copy-Item .env.example .env
```

For the built-in SQLite demonstration mode, leave `DATABASE_URL` blank in `.env` (or do not create `.env`), then run:

```powershell
python manage.py init-db
python manage.py seed-demo
python manage.py run
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Run tests with `python -m pytest -q`.

## MySQL setup

Create the database and a least-privilege user in MySQL, then set this line in `.env`:

```text
DATABASE_URL=mysql+pymysql://budget_user:replace_me@localhost:3306/home_budget
```

Apply the schema without dropping existing data with `python manage.py init-db`; alternatively review and run `schema.sql` in a MySQL 8 client. The included Alembic revision is `migrations/versions/20261029_0001_initial_schema.py`. MySQL connectivity was not available in this workspace, so it remains an external verification step.

## Vercel deployment

The repository includes `api/index.py` and `vercel.json` for Vercel's Python runtime. A public Vercel deployment requires a hosted MySQL database because serverless SQLite files are not durable. In the Vercel project settings, add `DATABASE_URL` and `SECRET_KEY` from the `.env.example` format, then deploy:

```powershell
npx vercel login
npx vercel --prod
```

Use the generated `*.vercel.app` URL only after Vercel reports a successful production deployment. Initialize the hosted database once with the schema/migration tooling before exposing the site publicly. The configuration excludes tests, documentation, presentation outputs, and local virtual environments from the function bundle.

## API summary

`GET /api/health`, `/api/dashboard`, `/api/transactions`, `/api/categories`, `/api/budgets`, `/api/analytics/monthly`, `/api/analytics/categories`, `/api/analytics/budgets`, and the CSV export endpoints are implemented. Full examples appear in [API documentation](docs/API_DOCUMENTATION.md).

## Security and limitations

Credentials come from environment variables and `.env` is ignored. SQLAlchemy parameterizes database operations; forms include a session CSRF token; server-side validation rejects invalid values; error responses avoid secrets and SQL; and CSV cells beginning with formula characters receive a leading apostrophe. Authentication is intentionally out of scope, so do not expose this prototype publicly. The application has no bank, payment-gateway, or financial-advice integration.

## Project documentation

See [the documentation index](docs/DELIVERABLE_TRACKER.md) for D1–D8 status, evidence, and remaining MySQL verification.
