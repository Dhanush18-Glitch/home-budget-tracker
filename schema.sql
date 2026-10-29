-- MySQL 8 schema for Home Budget (Expense Tracker) and Analysis System.
-- Set database credentials in DATABASE_URL; do not commit credentials.
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  kind VARCHAR(10) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_category_name_kind UNIQUE (name, kind),
  CONSTRAINT ck_category_kind CHECK (kind IN ('income','expense'))
);
CREATE TABLE IF NOT EXISTS transactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  transaction_date DATE NOT NULL,
  kind VARCHAR(10) NOT NULL,
  category_id INT NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  description VARCHAR(255) NOT NULL,
  payment_method VARCHAR(50) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_transaction_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
  CONSTRAINT ck_transaction_kind CHECK (kind IN ('income','expense')),
  CONSTRAINT ck_transaction_amount CHECK (amount > 0),
  INDEX ix_transactions_date_kind (transaction_date, kind), INDEX ix_transactions_category (category_id)
);
CREATE TABLE IF NOT EXISTS monthly_budgets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  category_id INT NOT NULL,
  month TINYINT NOT NULL,
  year SMALLINT NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_budget_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
  CONSTRAINT uq_budget_category_month_year UNIQUE (category_id, month, year),
  CONSTRAINT ck_budget_month CHECK (month BETWEEN 1 AND 12), CONSTRAINT ck_budget_amount CHECK (amount > 0),
  INDEX ix_budgets_category (category_id)
);
