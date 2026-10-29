# 10 Minute Demonstration Plan

| Time | Screen or evidence | What to show and say |
|---|---|---|
| 0:00–0:45 | README and project folder | State the household-budget problem, manual-data boundary, and stack. |
| 0:45–1:30 | `schema.sql` and ER diagram | Explain category-to-transaction and category-to-budget relationships, decimal amount fields, unique budget period, and restricted deletion. |
| 1:30–2:15 | Terminal | Run health endpoint and show `database: connected`. Explain that SQLite is the local demo and MySQL is configured by `DATABASE_URL`. |
| 2:15–3:30 | Dashboard | Select October 2026. Explain income, expenses, net savings, savings rate, allocated and remaining budget values. |
| 3:30–4:45 | Transactions | Create an expense such as ₹300 Groceries. Filter it, edit it, then delete it. Confirm dashboard totals change and return. |
| 4:45–5:45 | Categories and Budgets | Point out protected categories. Set or inspect the ₹5,000 Grocery budget and explain actual/budget × 100 utilization and actual−budget variance. |
| 5:45–7:10 | Analytics | Show all four charts. Explain that rent dominates the records, monthly trend uses stored months, and the Grocery actual bar exceeds budget in demo data. |
| 7:10–8:00 | API and CSV | Show a transaction POST example and CSV export. Mention validation and formula-injection escaping. |
| 8:00–9:00 | `pytest -q` and test report | Show six passed tests and name the covered invalid input, duplicate budget, zero-data, chart, CRUD, and export cases. |
| 9:00–10:00 | Limitations and conclusion | State lack of authentication/bank integration, local trusted use, and unverified MySQL connectivity. Conclude with the completed working data flow. |

Inspect database records via the Transactions page or `GET /api/transactions`; inspect October budget comparisons via `GET /api/analytics/budgets?year=2026&month=10`.
