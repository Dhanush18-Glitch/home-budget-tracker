from datetime import date, datetime
import secrets
import time
from flask import Blueprint, abort, flash, redirect, render_template, request, send_from_directory, session, url_for
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Category, MonthlyBudget, Transaction
from app.services.analytics import budget_comparison, category_summary, dashboard_metrics, monthly_trends, transactions_for_period
from app.services.charts import CHART_DIR, make_charts
from app.services.validation import ValidationError, clean_budget, clean_category, clean_transaction

web_bp = Blueprint("web", __name__)


@web_bp.before_app_request
def csrf_protection():
    if "csrf_token" not in session: session["csrf_token"] = secrets.token_urlsafe(24)
    if request.endpoint and request.endpoint.startswith("web.") and request.method in {"POST", "PUT", "DELETE"}:
        if request.form.get("csrf_token") != session["csrf_token"]: abort(400, "Invalid form token. Refresh the page and try again.")


@web_bp.app_context_processor
def inject_csrf(): return {"csrf_token": session.get("csrf_token", "")}


def selected_period():
    today = date.today()
    report_date = request.args.get("date", "").strip()
    if report_date:
        try:
            selected = date.fromisoformat(report_date)
            return selected.year, selected.month, selected
        except ValueError:
            flash("Date must use YYYY-MM-DD format.", "error")
    try:
        return int(request.args.get("year", today.year)), int(request.args.get("month", today.month)), None
    except ValueError:
        return today.year, today.month, None


@web_bp.get("/")
def dashboard():
    year, month, as_of = selected_period()
    records = transactions_for_period(year, month, as_of=as_of).all()
    chart_paths = make_charts(records, year, month, prefix="dashboard", trend_transactions=transactions_for_period(year, as_of=as_of).all(), as_of=as_of)
    chart_version = time.time_ns()
    return render_template("dashboard.html", metrics=dashboard_metrics(year, month, as_of=as_of), year=year, month=month,
                           selected_date=as_of.isoformat() if as_of else "",
                           charts={k: f"{url_for('web.chart_file', filename=v.name)}?v={chart_version}" for k, v in chart_paths.items()})


@web_bp.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        try:
            db.session.add(Transaction(**clean_transaction(request.form))); db.session.commit(); flash("Transaction recorded.", "success")
            return redirect(url_for("web.dashboard"))
        except ValidationError as exc: flash(str(exc), "error")
    q = Transaction.query.join(Transaction.category)
    kind = request.args.get("type"); search = request.args.get("q", "").strip()
    if kind in {"income", "expense"}: q = q.filter(Transaction.kind == kind)
    if request.args.get("category_id"): q = q.filter(Transaction.category_id == int(request.args["category_id"]))
    if search: q = q.filter(Transaction.description.ilike(f"%{search}%"))
    if request.args.get("from"): q = q.filter(Transaction.transaction_date >= request.args["from"])
    if request.args.get("to"): q = q.filter(Transaction.transaction_date <= request.args["to"])
    items = q.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).all()
    return render_template("transactions.html", transactions=items, categories=Category.query.order_by(Category.name).all(), filters=request.args)


@web_bp.route("/transactions/<int:transaction_id>/edit", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id) or abort(404)
    if request.method == "POST":
        try:
            for key, value in clean_transaction(request.form).items(): setattr(transaction, key, value)
            db.session.commit(); flash("Transaction updated.", "success"); return redirect(url_for("web.dashboard"))
        except ValidationError as exc: flash(str(exc), "error")
    return render_template("transaction_form.html", transaction=transaction, categories=Category.query.order_by(Category.name).all())


@web_bp.post("/transactions/<int:transaction_id>/delete")
def delete_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id) or abort(404)
    db.session.delete(transaction); db.session.commit(); flash("Transaction deleted.", "success")
    return redirect(url_for("web.dashboard"))


@web_bp.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        try:
            db.session.add(Category(**clean_category(request.form))); db.session.commit(); flash("Category added.", "success")
        except ValidationError as exc: flash(str(exc), "error")
        except IntegrityError: db.session.rollback(); flash("That category and type already exist.", "error")
        return redirect(url_for("web.categories"))
    return render_template("categories.html", categories=Category.query.order_by(Category.kind, Category.name).all())


@web_bp.post("/categories/<int:category_id>/delete")
def delete_category(category_id):
    category = db.session.get(Category, category_id) or abort(404)
    if category.transactions or category.budgets: flash("This category is in use and cannot be deleted.", "error")
    else: db.session.delete(category); db.session.commit(); flash("Category deleted.", "success")
    return redirect(url_for("web.categories"))


@web_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id):
    category = db.session.get(Category, category_id) or abort(404)
    if request.method == "POST":
        try:
            values = clean_category(request.form)
            if (category.transactions or category.budgets) and values["kind"] != category.kind:
                raise ValidationError("The type of a category in use by transactions or budgets cannot change.")
            category.name, category.kind = values["name"], values["kind"]
            db.session.commit(); flash("Category updated.", "success"); return redirect(url_for("web.categories"))
        except ValidationError as exc: flash(str(exc), "error")
        except IntegrityError: db.session.rollback(); flash("That category and type already exist.", "error")
    return render_template("category_form.html", category=category)


@web_bp.route("/budgets", methods=["GET", "POST"])
def budgets():
    year, month, _ = selected_period()
    if request.method == "POST":
        try:
            db.session.add(MonthlyBudget(**clean_budget(request.form))); db.session.commit(); flash("Budget saved.", "success")
        except ValidationError as exc: flash(str(exc), "error")
        except IntegrityError: db.session.rollback(); flash("A budget already exists for that category and period.", "error")
        return redirect(url_for("web.dashboard", year=year, month=month))
    return render_template("budgets.html", comparisons=budget_comparison(year, month), year=year, month=month,
                           categories=Category.query.filter_by(kind="expense").order_by(Category.name).all())


@web_bp.post("/budgets/<int:budget_id>/delete")
def delete_budget(budget_id):
    budget = db.session.get(MonthlyBudget, budget_id) or abort(404)
    year, month = budget.year, budget.month
    db.session.delete(budget); db.session.commit(); flash("Budget deleted.", "success")
    return redirect(url_for("web.dashboard", year=year, month=month))


@web_bp.route("/budgets/<int:budget_id>/edit", methods=["GET", "POST"])
def edit_budget(budget_id):
    budget = db.session.get(MonthlyBudget, budget_id) or abort(404)
    if request.method == "POST":
        try:
            for key, value in clean_budget(request.form).items(): setattr(budget, key, value)
            db.session.commit(); flash("Budget updated.", "success")
            return redirect(url_for("web.dashboard", year=budget.year, month=budget.month))
        except ValidationError as exc: flash(str(exc), "error")
        except IntegrityError: db.session.rollback(); flash("A budget already exists for that category and period.", "error")
    return render_template("budget_form.html", budget=budget, categories=Category.query.filter_by(kind="expense").order_by(Category.name).all())


@web_bp.get("/analytics")
def analytics():
    year, month, _ = selected_period(); records = transactions_for_period(year, month).all()
    chart_paths = make_charts(records, year, month, prefix="live", trend_transactions=transactions_for_period(year).all())
    return render_template("analytics.html", categories=category_summary(records), trends=monthly_trends(Transaction.query.all()),
                           charts={k: f"{url_for('web.chart_file', filename=v.name)}?v={time.time_ns()}" for k, v in chart_paths.items()}, year=year, month=month)


@web_bp.get("/reports")
def reports():
    year, month, _ = selected_period()
    return render_template("reports.html", year=year, month=month)


@web_bp.get("/charts/<path:filename>")
def chart_file(filename):
    return send_from_directory(str(CHART_DIR), filename)


@web_bp.get("/settings")
def settings(): return render_template("settings.html")
