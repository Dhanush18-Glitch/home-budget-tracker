import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from app.services.analytics import category_summary, monthly_trends, budget_comparison, frame_from_transactions


# Vercel functions allow writes only beneath /tmp. Local use keeps generated
# evidence in the project artifacts folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHART_DIR = Path(os.getenv("CHART_OUTPUT_DIR", "/tmp/home_budget_charts" if os.getenv("VERCEL") else PROJECT_ROOT / "artifacts" / "charts"))


def _save(fig, name):
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    path = CHART_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return path


def make_charts(transactions, year=None, month=None, prefix="live", trend_transactions=None, as_of=None):
    labels = f"{year}-{month:02d}" if year and month else "all recorded months"
    categories = category_summary(transactions)
    # Distribution and budget charts use the selected month; trends use every
    # stored month in the selected year when the caller supplies that scope.
    trends = monthly_trends(trend_transactions if trend_transactions is not None else transactions)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if categories:
        ax.pie([float(x["amount"]) for x in categories], labels=[x["category"] for x in categories], autopct="%1.1f%%")
        ax.set_title("Expense Distribution by Category")
    else:
        ax.text(.5, .5, "No expense data for selected period", ha="center", va="center")
        ax.set_axis_off()
    output = {"expense_distribution": _save(fig, f"{prefix}_expense_distribution.png")}
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if trends:
        months = [x["month"] for x in trends]
        ax.plot(months, [float(x["income"]) for x in trends], marker="o", label="Income")
        ax.plot(months, [float(x["expenses"]) for x in trends], marker="o", label="Expenses")
        ax.legend(); ax.set_ylabel("Amount (INR)"); ax.set_title("Monthly Income Versus Expenses")
    else: ax.text(.5, .5, "No transaction data", ha="center", va="center"); ax.set_axis_off()
    output["income_expenses"] = _save(fig, f"{prefix}_income_expenses.png")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if trends:
        ax.plot([x["month"] for x in trends], [float(x["savings"]) for x in trends], marker="o", color="#27864a")
        ax.axhline(0, color="black", linewidth=.7); ax.set_ylabel("Amount (INR)"); ax.set_title("Monthly Savings Trend")
    else: ax.text(.5, .5, "No transaction data", ha="center", va="center"); ax.set_axis_off()
    output["savings_trend"] = _save(fig, f"{prefix}_savings_trend.png")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    comparisons = budget_comparison(year, month, as_of=as_of) if year and month else []
    if comparisons:
        names = [x["category"] for x in comparisons]; positions = range(len(names))
        ax.bar([x-.2 for x in positions], [float(x["budget"]) for x in comparisons], .4, label="Budget")
        ax.bar([x+.2 for x in positions], [float(x["actual"]) for x in comparisons], .4, label="Actual")
        ax.set_xticks(list(positions), names, rotation=25, ha="right"); ax.set_ylabel("Amount (INR)"); ax.legend()
        ax.set_title(f"Budget Versus Actual Spending ({labels})")
    else: ax.text(.5, .5, "No budget data for selected period", ha="center", va="center"); ax.set_axis_off()
    output["budget_actual"] = _save(fig, f"{prefix}_budget_actual.png")
    return output
