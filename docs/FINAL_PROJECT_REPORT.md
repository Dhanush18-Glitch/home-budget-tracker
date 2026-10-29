# Final Project Report

## Abstract and introduction

The Home Budget Expense Tracker and Analysis System is a Flask-based local application that converts manually entered household income and expense records into monthly summaries, category analysis, budget controls, exports, and charts. The project addresses the difficulty of seeing savings and overspending across scattered personal records.

## Problem, objectives, scope, and requirements

The system records valid dated transactions, organizes them into income and expense categories, accepts monthly expense budgets, and calculates savings and budget status. It supports a trusted single local user. It intentionally excludes bank integrations, payment processing, credential storage, financial advice, multi-user authentication, and forecasting.

## Architecture and database design

Flask templates and JSON blueprints call validation, analytics, chart, reporting, and seed services. SQLAlchemy models map `categories`, `transactions`, and `monthly_budgets` to MySQL-compatible tables. The schema supplies primary keys, foreign keys, unique constraints, date/type indexing, `DECIMAL(12,2)` amounts, and restricted category deletion. SQLite supports local demonstration/tests, but MySQL remains the production database target. See [ER diagram](ER_DIAGRAM.md).

## Implementation and formulas

Transactions support create, read, update, delete, filtering, search, sorting, API pagination, and accurate filtered totals. Categories prevent same-type duplicates and protected deletions. Budgets prevent duplicate category-month-year records. Net savings equals income minus expenses; savings rate is savings/income × 100; budget utilization is actual/budget × 100; remaining budget is budget−actual; and variance is actual−budget. Zero-income rates return 0%. See [analysis methodology](ANALYSIS_METHODOLOGY.md).

## Data analysis and visualizations

Pandas groups transactions by category and pivots records by month/type. NumPy handles guarded rates. Matplotlib generates expense distribution, monthly income versus expenses, savings trend, and budget versus actual charts from stored demo records. In October demo data, Grocery spending is ₹5,750 against a ₹5,000 budget, which demonstrates an over-budget result. The charts are real generated files, not static placeholders.

## Testing and demonstration

The final executed pytest run on 2026-10-29 passed 8 tests in 5.09 seconds. Covered behavior includes default seed categories, transaction CRUD, invalid validation, budget conflicts/overruns, formula-safe and filtered CSV exports, report summaries, date-aware dashboard values, and generated chart routes. Details and warnings are recorded in [the test report](TEST_REPORT.md). The live demonstration sequence appears in [the demonstration plan](DEMONSTRATION_PLAN.md).

## Limitations and future work

The local prototype has no authentication, receipt capture, scheduled reminders, bank feeds, multi-currency support, or reconciliation. MySQL connectivity is implemented but unverified without a running server and credentials. A future version could add authenticated users, audited role-based access, receipt attachments, import review, and better dashboard period comparison.

## Conclusion and references

The project meets the academic requirement for a maintainable Flask prototype with persisted records, descriptive analytics, chart evidence, reporting, validation, and test evidence. Technical references: [Flask documentation](https://flask.palletsprojects.com/), [SQLAlchemy documentation](https://docs.sqlalchemy.org/), [Pandas documentation](https://pandas.pydata.org/docs/), [NumPy documentation](https://numpy.org/doc/), and [Matplotlib documentation](https://matplotlib.org/stable/).
