# API Documentation

All successful responses are JSON except CSV exports. Validation errors use HTTP 400 with `{"error":{"code":"validation_error","message":"..."}}`; missing IDs use 404; duplicate category/budget conflicts use 409.

| Method and path | Purpose | Parameters and validation |
|---|---|---|
| GET `/api/health` | Database health | Returns engine name or 503 |
| GET `/api/dashboard?year=2026&month=10` | Period KPIs | Calendar period |
| GET/POST `/api/transactions` | List/create records | List: `type`, `category_id`, `from`, `to`, `q`, `year`, `month`, `sort`, `page`, `per_page`; create: date, type, category_id, positive amount, description, optional payment_method |
| GET/PUT/DELETE `/api/transactions/{id}` | Read/update/delete record | Same validated body for PUT |
| GET/POST `/api/categories` | List/create categories | `name` <=80 chars, type income/expense |
| GET/PUT/DELETE `/api/categories/{id}` | Read/update/delete category | Referenced categories return 409 on delete |
| GET/POST `/api/budgets` | List/create period budgets | positive amount, existing expense category, month 1–12, year 2000–2100 |
| GET/PUT/DELETE `/api/budgets/{id}` | Read/update/delete budget | Duplicate category/month/year returns 409 |
| GET `/api/analytics/monthly` | All-month trend | None |
| GET `/api/analytics/categories` | Period category totals | `year`, `month` |
| GET `/api/analytics/budgets` | Period budget comparison | `year`, `month` |
| POST `/api/charts?year=2026&month=10` | Generate four chart files | Selected period |
| GET `/api/exports/transactions.csv` | Filtered transaction CSV | Uses the same filters as the transaction listing and makes formula-like cells safe |
| GET `/api/exports/budgets.csv?year=2026&month=10` | Budget CSV | Selected period |
| GET `/api/exports/monthly-summary.csv` | Monthly income/expense/savings CSV | All stored months |
| GET `/api/exports/categories.csv?year=2026&month=10` | Category summary CSV | Selected period |

Example creation request:

```json
POST /api/transactions
{"date":"2026-10-30","type":"expense","category_id":7,"amount":"249.50","description":"Bus pass","payment_method":"UPI"}
```

Example 201 response: `{"id":23,"date":"2026-10-30","type":"expense","amount":"249.50",...}`. Categories must match the record type; zero/negative amounts, malformed dates, missing fields, and unsupported kinds are rejected.
