# User Guide

1. Run `python manage.py init-db`, `python manage.py seed-demo`, and `python manage.py run`, then open `http://127.0.0.1:5000`.
2. Choose a month and year on the dashboard to read the stored income, expenses, savings, rate, budget allocation, and budget alerts.
3. On Transactions, add income or expense records. Select a category matching its type, use a positive amount, then use search/date/type filters to inspect entries. Edit or delete records from the same table.
4. On Categories, add a named income or expense category. Used categories remain protected so historic values stay meaningful.
5. On Budgets, select the period, choose an expense category, and save a positive allocation. The table marks under, approaching (80%+), over, and unbudgeted spend states.
6. On Analytics, read the selected period’s category table and generated charts. Use `/api/exports/transactions.csv` or `/api/exports/budgets.csv?year=2026&month=10` for CSV output.

If the dashboard is empty, load safe synthetic records with `python manage.py seed-demo`. Do not use this prototype to store bank passwords or expose it to the public internet.
