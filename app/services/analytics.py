from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import pandas as pd
from sqlalchemy import extract
from app.models import MonthlyBudget, Transaction


MONEY = Decimal("0.01")


def money(value):
    return Decimal(str(value or 0)).quantize(MONEY, rounding=ROUND_HALF_UP)


def transactions_for_period(year=None, month=None, as_of=None, query=None):
    q = Transaction.query.join(Transaction.category)
    if year:
        q = q.filter(extract("year", Transaction.transaction_date) == int(year))
    if month:
        q = q.filter(extract("month", Transaction.transaction_date) == int(month))
    if as_of:
        q = q.filter(Transaction.transaction_date <= as_of)
    return q


def frame_from_transactions(transactions):
    rows = [{"date": item.transaction_date, "type": item.kind, "category": item.category.name,
             "amount": float(item.amount), "description": item.description} for item in transactions]
    return pd.DataFrame(rows, columns=["date", "type", "category", "amount", "description"])


def calculate_summary(transactions):
    frame = frame_from_transactions(transactions)
    if frame.empty:
        return {"income": money(0), "expenses": money(0), "savings": money(0), "savings_rate": 0.0,
                "transaction_count": 0, "average_transaction": money(0), "highest_spending_category": None}
    income = money(frame.loc[frame.type == "income", "amount"].sum())
    expenses = money(frame.loc[frame.type == "expense", "amount"].sum())
    savings = money(income - expenses)
    rate = float(np.divide(float(savings) * 100, float(income))) if income else 0.0
    expense_groups = frame[frame.type == "expense"].groupby("category").amount.sum()
    highest = expense_groups.idxmax() if not expense_groups.empty else None
    return {"income": income, "expenses": expenses, "savings": savings, "savings_rate": round(rate, 2),
            "transaction_count": len(frame), "average_transaction": money(frame.amount.mean()),
            "highest_spending_category": highest}


def category_summary(transactions):
    frame = frame_from_transactions(transactions)
    if frame.empty:
        return []
    expenses = frame[frame.type == "expense"]
    if expenses.empty:
        return []
    totals = expenses.groupby("category", as_index=False).amount.sum().sort_values("amount", ascending=False)
    total = totals.amount.sum()
    return [{"category": row.category, "amount": str(money(row.amount)),
             "percentage": round(float(np.divide(row.amount * 100, total)) if total else 0, 2)}
            for row in totals.itertuples(index=False)]


def monthly_trends(transactions):
    frame = frame_from_transactions(transactions)
    if frame.empty:
        return []
    frame["month"] = pd.to_datetime(frame.date).dt.to_period("M").astype(str)
    pivot = frame.pivot_table(index="month", columns="type", values="amount", aggfunc="sum", fill_value=0)
    pivot = pivot.reindex(columns=["income", "expense"], fill_value=0)
    return [{"month": month, "income": str(money(row.income)), "expenses": str(money(row.expense)),
             "savings": str(money(row.income - row.expense))} for month, row in pivot.iterrows()]


def budget_comparison(year, month, as_of=None):
    transactions = transactions_for_period(year, month, as_of=as_of).all()
    actuals = {row["category"]: money(row["amount"]) for row in category_summary(transactions)}
    budgets = MonthlyBudget.query.filter_by(year=year, month=month).join(MonthlyBudget.category).all()
    result, budgeted_names = [], set()
    for budget in budgets:
        actual = actuals.get(budget.category.name, money(0))
        allocation = money(budget.amount)
        utilization = round(float(np.divide(float(actual) * 100, float(allocation))), 2) if allocation else 0.0
        status = "over" if actual > allocation else "approaching" if utilization >= 80 else "under"
        result.append({"id": budget.id, "category": budget.category.name, "budget": allocation, "actual": actual,
                       "remaining": money(allocation - actual), "variance": money(actual - allocation),
                       "utilization": utilization, "status": status})
        budgeted_names.add(budget.category.name)
    for name, actual in actuals.items():
        if name not in budgeted_names:
            result.append({"id": None, "category": name, "budget": money(0), "actual": actual,
                           "remaining": money(-actual), "variance": actual, "utilization": None,
                           "status": "unbudgeted"})
    return sorted(result, key=lambda item: item["category"])


def dashboard_metrics(year, month, as_of=None):
    transactions = transactions_for_period(year, month, as_of=as_of).all()
    summary = calculate_summary(transactions)
    comparisons = budget_comparison(year, month, as_of=as_of)
    allocated = sum((item["budget"] for item in comparisons), money(0))
    actual_budgeted = sum((item["actual"] for item in comparisons if item["budget"]), money(0))
    summary.update({"allocated_budget": money(allocated), "remaining_budget": money(allocated - actual_budgeted),
                    "over_budget": [item for item in comparisons if item["status"] == "over"],
                    "comparisons": comparisons})
    return summary
