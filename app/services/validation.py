from datetime import date
from decimal import Decimal, InvalidOperation
from app.models import Category


class ValidationError(ValueError):
    pass


def clean_transaction(data):
    required = ("date", "type", "category_id", "amount", "description")
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise ValidationError("Missing required fields: " + ", ".join(missing))
    try:
        transaction_date = date.fromisoformat(str(data["date"]))
    except (TypeError, ValueError):
        raise ValidationError("Date must use YYYY-MM-DD format.")
    kind = str(data["type"]).lower()
    if kind not in {"income", "expense"}:
        raise ValidationError("Type must be income or expense.")
    try:
        category_id = int(data["category_id"])
        amount = Decimal(str(data["amount"])).quantize(Decimal("0.01"))
    except (ValueError, InvalidOperation):
        raise ValidationError("Category and amount must be valid values.")
    if amount <= 0:
        raise ValidationError("Amount must be greater than zero.")
    category = Category.query.get(category_id)
    if not category or category.kind != kind:
        raise ValidationError("Choose a category matching the transaction type.")
    description = str(data["description"]).strip()
    if len(description) > 255:
        raise ValidationError("Description must be 255 characters or fewer.")
    method = str(data.get("payment_method", "")).strip() or None
    if method and len(method) > 50:
        raise ValidationError("Payment method must be 50 characters or fewer.")
    return {"transaction_date": transaction_date, "kind": kind, "category_id": category_id,
            "amount": amount, "description": description, "payment_method": method}


def clean_category(data):
    name = str(data.get("name", "")).strip()
    kind = str(data.get("type", data.get("kind", ""))).lower()
    if not name or len(name) > 80:
        raise ValidationError("Category name is required and must be 80 characters or fewer.")
    if kind not in {"income", "expense"}:
        raise ValidationError("Category type must be income or expense.")
    return {"name": name, "kind": kind}


def clean_budget(data):
    try:
        category_id, month, year = int(data["category_id"]), int(data["month"]), int(data["year"])
        amount = Decimal(str(data["amount"])).quantize(Decimal("0.01"))
    except (KeyError, ValueError, InvalidOperation):
        raise ValidationError("Category, month, year, and amount are required.")
    category = Category.query.get(category_id)
    if not category or category.kind != "expense":
        raise ValidationError("Budget categories must be existing expense categories.")
    if not 1 <= month <= 12 or not 2000 <= year <= 2100:
        raise ValidationError("Month or year is outside the supported range.")
    if amount <= 0:
        raise ValidationError("Budget amount must be greater than zero.")
    return {"category_id": category_id, "month": month, "year": year, "amount": amount}
