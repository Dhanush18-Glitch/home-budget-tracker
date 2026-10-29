# Analysis Methodology

The analytics service retrieves records through SQLAlchemy, converts them into a Pandas DataFrame with date, type, category, amount, and description columns, then uses `groupby`, `pivot_table`, boolean filters, and sums. NumPy performs guarded ratios. Monetary values are converted back to two-decimal `Decimal` values for displayed results.

## Formulas

| Metric | Formula |
|---|---|
| Net savings | income − expenses |
| Savings rate | `(net savings / income) × 100`; 0 when income is zero |
| Category share | `(category expenses / all expenses) × 100` |
| Budget utilization | `(actual category expenses / budget) × 100` |
| Remaining budget | budget − actual expenses |
| Budget variance | actual expenses − budget |

Monthly trends pivot income and expense by `YYYY-MM`; savings is their difference. Category summaries include expenses only. The comparison baseline uses the immediately earlier selected month when a caller compares periods externally; the current web view presents selected-period values. Empty records produce zero totals and empty summary lists. Missing months are not invented, and zero income produces a 0% savings rate rather than a division error. Ratios are rounded to two decimals only for output.

## Verified sample-data summary

The repeatable synthetic demo seed produced these runtime-derived totals:

| Month | Income INR | Expenses INR | Savings INR |
|---|---:|---:|---:|
| 2026-07 | 65,000.00 | 24,700.00 | 40,300.00 |
| 2026-08 | 73,500.00 | 27,600.00 | 45,900.00 |
| 2026-09 | 65,000.00 | 28,400.00 | 36,600.00 |
| 2026-10 | 77,000.00 | 31,250.00 | 45,750.00 |

Illustrative check: a ₹5,000 budget and ₹5,750 actual expense yield ₹750 overspending, ₹−750 remaining budget, ₹750 variance, and 115% utilization. The application calculates these values from selected database records; this line is an explanatory example, not a stored dashboard value.

Limitations: analytics reflects entered records only. It neither validates receipts nor predicts future spending.
