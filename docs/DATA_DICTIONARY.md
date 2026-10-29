# Data Dictionary

| Table | Field | Type | Meaning and rule |
|---|---|---|---|
| categories | id | integer | Primary key |
| categories | name | varchar(80) | Category label; unique with kind |
| categories | kind | varchar(10) | `income` or `expense` |
| transactions | id | integer | Primary key / transaction ID |
| transactions | transaction_date | date | Required ISO date; indexed |
| transactions | kind | varchar(10) | Required `income` or `expense` |
| transactions | category_id | integer | Required FK to categories; restricted deletion |
| transactions | amount | decimal(12,2) | Required positive fixed-precision amount |
| transactions | description | varchar(255) | Required user explanation |
| transactions | payment_method | varchar(50) | Optional method |
| monthly_budgets | id | integer | Primary key |
| monthly_budgets | category_id | integer | Required expense-category FK |
| monthly_budgets | month/year | integer | Calendar period; one budget per category/month/year |
| monthly_budgets | amount | decimal(12,2) | Required positive allocation |

Timestamps (`created_at`, `updated_at`) support audit context. Default data contains six income categories and twelve expense categories. `python manage.py seed-demo` creates synthetic July–October 2026 records only when no transaction already exists, preventing duplicate demo rows.
