from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Category, MonthlyBudget, Transaction
from app.services.analytics import budget_comparison, calculate_summary, category_summary, dashboard_metrics, monthly_trends, transactions_for_period
from app.services.charts import make_charts
from app.services.reports import csv_response
from app.services.validation import ValidationError, clean_budget, clean_category, clean_transaction

api_bp = Blueprint("api", __name__)


def body(): return request.get_json(silent=True) or request.form.to_dict()
def error(message, status=400): return jsonify(error={"code": "validation_error" if status == 400 else "not_found", "message": message}), status
def period():
    now = datetime.now(); return int(request.args.get("year", now.year)), int(request.args.get("month", now.month))


def filtered_transactions_query():
    """Shared filter rules keep list totals and CSV output aligned."""
    q = Transaction.query.join(Transaction.category)
    if request.args.get("type") in {"income", "expense"}: q = q.filter(Transaction.kind == request.args["type"])
    if request.args.get("category_id"): q = q.filter(Transaction.category_id == int(request.args["category_id"]))
    if request.args.get("from"): q = q.filter(Transaction.transaction_date >= request.args["from"])
    if request.args.get("to"): q = q.filter(Transaction.transaction_date <= request.args["to"])
    if request.args.get("q"): q = q.filter(Transaction.description.ilike(f"%{request.args['q']}%"))
    year, month = request.args.get("year"), request.args.get("month")
    if year: q = q.filter(db.extract("year", Transaction.transaction_date) == int(year))
    if month: q = q.filter(db.extract("month", Transaction.transaction_date) == int(month))
    return q


@api_bp.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify(status="ok", database="connected", engine=db.engine.url.get_backend_name())
    except Exception:
        return jsonify(status="degraded", database="unavailable"), 503


@api_bp.get("/dashboard")
def dashboard():
    year, month = period(); as_of = None
    if request.args.get("date"):
        try:
            as_of = datetime.strptime(request.args["date"], "%Y-%m-%d").date()
            year, month = as_of.year, as_of.month
        except ValueError:
            return error("Date must use YYYY-MM-DD format.")
    data = dashboard_metrics(year, month, as_of=as_of)
    for key in ("income", "expenses", "savings", "average_transaction", "allocated_budget", "remaining_budget"):
        data[key] = str(data[key])
    return jsonify(period={"year": year, "month": month, "as_of": as_of.isoformat() if as_of else None}, **data)


@api_bp.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "GET":
        kind = request.args.get("type")
        q = Category.query
        if kind: q = q.filter_by(kind=kind)
        return jsonify([item.as_dict() for item in q.order_by(Category.kind, Category.name).all()])
    try:
        values = clean_category(body()); category = Category(**values); db.session.add(category); db.session.commit()
        return jsonify(category.as_dict()), 201
    except ValidationError as exc: return error(str(exc))
    except IntegrityError: db.session.rollback(); return error("A category with this name and type already exists.", 409)


@api_bp.route("/categories/<int:category_id>", methods=["GET", "PUT", "DELETE"])
def category_detail(category_id):
    category = db.session.get(Category, category_id)
    if not category: return error("Category not found.", 404)
    if request.method == "GET": return jsonify(category.as_dict())
    if request.method == "DELETE":
        if category.transactions or category.budgets: return error("Categories referenced by transactions or budgets cannot be deleted.", 409)
        db.session.delete(category); db.session.commit(); return "", 204
    try:
        values = clean_category(body()); category.name = values["name"]; category.kind = values["kind"]; db.session.commit(); return jsonify(category.as_dict())
    except ValidationError as exc: return error(str(exc))
    except IntegrityError: db.session.rollback(); return error("A category with this name and type already exists.", 409)


@api_bp.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        try:
            transaction = Transaction(**clean_transaction(body())); db.session.add(transaction); db.session.commit(); return jsonify(transaction.as_dict()), 201
        except ValidationError as exc: return error(str(exc))
    q = filtered_transactions_query()
    sort = request.args.get("sort", "date_desc"); order = Transaction.amount.asc() if sort == "amount_asc" else Transaction.amount.desc() if sort == "amount_desc" else Transaction.transaction_date.asc() if sort == "date_asc" else Transaction.transaction_date.desc()
    page = max(int(request.args.get("page", 1)), 1); per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)
    result = q.order_by(order, Transaction.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    all_filtered = q.all(); summary = calculate_summary(all_filtered)
    return jsonify(items=[x.as_dict() for x in result.items], page=page, pages=result.pages, total=result.total,
                   totals={k: str(v) if hasattr(v, "quantize") else v for k, v in summary.items()})


@api_bp.route("/transactions/<int:transaction_id>", methods=["GET", "PUT", "DELETE"])
def transaction_detail(transaction_id):
    transaction = db.session.get(Transaction, transaction_id)
    if not transaction: return error("Transaction not found.", 404)
    if request.method == "GET": return jsonify(transaction.as_dict())
    if request.method == "DELETE": db.session.delete(transaction); db.session.commit(); return "", 204
    try:
        for key, value in clean_transaction(body()).items(): setattr(transaction, key, value)
        db.session.commit(); return jsonify(transaction.as_dict())
    except ValidationError as exc: return error(str(exc))


@api_bp.route("/budgets", methods=["GET", "POST"])
def budgets():
    if request.method == "POST":
        try:
            budget = MonthlyBudget(**clean_budget(body())); db.session.add(budget); db.session.commit(); return jsonify(budget.as_dict()), 201
        except ValidationError as exc: return error(str(exc))
        except IntegrityError: db.session.rollback(); return error("A budget already exists for this category and period.", 409)
    year, month = period(); return jsonify([x.as_dict() for x in MonthlyBudget.query.filter_by(year=year, month=month).all()])


@api_bp.route("/budgets/<int:budget_id>", methods=["GET", "PUT", "DELETE"])
def budget_detail(budget_id):
    budget = db.session.get(MonthlyBudget, budget_id)
    if not budget: return error("Budget not found.", 404)
    if request.method == "GET": return jsonify(budget.as_dict())
    if request.method == "DELETE": db.session.delete(budget); db.session.commit(); return "", 204
    try:
        for key, value in clean_budget(body()).items(): setattr(budget, key, value)
        db.session.commit(); return jsonify(budget.as_dict())
    except ValidationError as exc: return error(str(exc))
    except IntegrityError: db.session.rollback(); return error("A budget already exists for this category and period.", 409)


@api_bp.get("/analytics/monthly")
def monthly_analytics(): return jsonify(monthly_trends(Transaction.query.all()))


@api_bp.get("/analytics/categories")
def category_analytics():
    year, month = period(); return jsonify(category_summary(transactions_for_period(year, month).all()))


@api_bp.get("/analytics/budgets")
def budget_analytics():
    year, month = period(); data = budget_comparison(year, month)
    for row in data:
        for key in ("budget", "actual", "remaining", "variance"): row[key] = str(row[key])
    return jsonify(data)


@api_bp.post("/charts")
def charts():
    year, month = period(); paths = make_charts(transactions_for_period(year, month).all(), year, month, trend_transactions=transactions_for_period(year).all())
    return jsonify({name: str(path).replace("\\", "/") for name, path in paths.items()}), 201


@api_bp.get("/exports/transactions.csv")
def export_transactions():
    rows = [x.as_dict() for x in filtered_transactions_query().order_by(Transaction.transaction_date.desc()).all()]
    return csv_response("transactions.csv", ["ID", "Date", "Type", "Category", "Amount", "Description", "Payment method"],
                        [[x["id"], x["date"], x["type"], x["category"], x["amount"], x["description"], x["payment_method"]] for x in rows])


@api_bp.get("/exports/budgets.csv")
def export_budgets():
    year, month = period(); rows = budget_comparison(year, month)
    return csv_response(f"budgets_{year}_{month:02d}.csv", ["Category", "Budget", "Actual", "Remaining", "Utilization %", "Status"],
                        [[x["category"], x["budget"], x["actual"], x["remaining"], x["utilization"], x["status"]] for x in rows])


@api_bp.get("/exports/monthly-summary.csv")
def export_monthly_summary():
    rows = monthly_trends(Transaction.query.all())
    return csv_response("monthly_summary.csv", ["Month", "Income", "Expenses", "Savings"],
                        [[x["month"], x["income"], x["expenses"], x["savings"]] for x in rows])


@api_bp.get("/exports/categories.csv")
def export_categories():
    year, month = period(); rows = category_summary(transactions_for_period(year, month).all())
    return csv_response(f"category_summary_{year}_{month:02d}.csv", ["Category", "Expenses", "Contribution %"],
                        [[x["category"], x["amount"], x["percentage"]] for x in rows])
