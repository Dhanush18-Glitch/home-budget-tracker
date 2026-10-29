# Entity Relationship Diagram

```mermaid
erDiagram
  CATEGORIES ||--o{ TRANSACTIONS : classifies
  CATEGORIES ||--o{ MONTHLY_BUDGETS : limits
  CATEGORIES {
    int id PK
    varchar name
    varchar kind
    datetime created_at
  }
  TRANSACTIONS {
    int id PK
    date transaction_date
    varchar kind
    int category_id FK
    decimal amount
    varchar description
    varchar payment_method
    datetime created_at
    datetime updated_at
  }
  MONTHLY_BUDGETS {
    int id PK
    int category_id FK
    int month
    int year
    decimal amount
    datetime created_at
    datetime updated_at
  }
```

`categories` has a unique `(name, kind)` pair. `monthly_budgets` has a unique `(category_id, month, year)` triplet. Foreign keys use `RESTRICT`, so a category used by a transaction or budget remains available for historic reporting. `transactions` has a date/type index; category and budget foreign-key columns are indexed by the ORM schema. See [schema.sql](../schema.sql) for the MySQL setup script and [the data dictionary](DATA_DICTIONARY.md) for field meanings.
