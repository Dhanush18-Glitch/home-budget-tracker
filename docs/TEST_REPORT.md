# Test Report

## Execution record

Executed on 2026-10-29 with Python 3.12.14 in a local temporary verification virtual environment because OneDrive held a lock while pip was writing the workspace `.venv`. Command: `python -m pytest -q`.

**Actual final result: 8 passed in 5.09 seconds.** Pytest reported 184 warnings, primarily third-party Matplotlib/Pyparsing deprecation messages and SQLAlchemy notices about naive timestamp defaults; no test failed. MySQL connection testing is unverified because no MySQL server credentials were configured.

| Case | Expected outcome | Actual outcome | Status |
|---|---|---|---|
| Health and default categories | Health is 200; 18 defaults exist | Returned 200 and 18 categories | Passed |
| Transaction CRUD and filter total | Create, filter, update, delete persist correctly | API completed lifecycle and 1000.50 filtered income total | Passed |
| Invalid transaction | Bad date, wrong category type, and zero amount fail | Returned 400 | Passed |
| Duplicate budget and overspend | Duplicate fails; 150 on 100 gives 150%/over | Returned 409 and expected indicator | Passed |
| CSV formula injection | Formula-like description is escaped | Export contains leading apostrophe | Passed |
| Report exports and filters | Filtered and summary CSV files match intended scope | Expense filter excluded income; monthly/category CSV endpoints returned 200 | Passed |
| Date-aware dashboard and charts | Dashboard accepts an as-of date and serves generated charts | Date filter applied; dashboard chart image route returned 200 | Passed |
| Empty values and charts | Empty month returns zero values; charts still generate | Four no-data-safe chart outputs returned | Passed |

Run the suite with `python -m pip install -r requirements.txt -r requirements-dev.txt` followed by `python -m pytest -q`. Unexecuted: a real MySQL network connection, browser automation, and a physical application restart test against a MySQL server. SQLite persistence is exercised by the same database configuration path and manual seed/start commands, but that does not verify MySQL infrastructure.
