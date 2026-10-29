from datetime import date
from decimal import Decimal
from app.extensions import db
from app.models import Category, MonthlyBudget, Transaction

INCOME = ["Salary", "Freelance", "Business Income", "Investments", "Gifts", "Other Income"]
EXPENSE = ["Groceries", "Rent and Housing", "Transportation", "Healthcare", "Education", "Utilities", "Entertainment", "Shopping", "Dining", "Insurance", "Personal Care", "Miscellaneous"]


def seed_defaults():
    for kind, names in (("income", INCOME), ("expense", EXPENSE)):
        for name in names:
            if not Category.query.filter_by(name=name, kind=kind).first():
                db.session.add(Category(name=name, kind=kind))
    db.session.commit()


def seed_demo_data():
    if Transaction.query.first(): return False
    by_name = {c.name: c for c in Category.query.all()}
    samples = [("2026-07-01", "income", "Salary", "65000", "July salary"), ("2026-07-04", "expense", "Rent and Housing", "18000", "Monthly rent"),
        ("2026-07-11", "expense", "Groceries", "4500", "Household groceries"), ("2026-07-19", "expense", "Utilities", "2200", "Electricity and internet"),
        ("2026-08-01", "income", "Salary", "65000", "August salary"), ("2026-08-05", "income", "Freelance", "8500", "Website work"),
        ("2026-08-05", "expense", "Rent and Housing", "18000", "Monthly rent"), ("2026-08-13", "expense", "Groceries", "5200", "Household groceries"),
        ("2026-08-18", "expense", "Transportation", "2800", "Fuel and metro"), ("2026-08-24", "expense", "Dining", "1600", "Family dinner"),
        ("2026-09-01", "income", "Salary", "65000", "September salary"), ("2026-09-03", "expense", "Rent and Housing", "18000", "Monthly rent"),
        ("2026-09-10", "expense", "Groceries", "6100", "Festival groceries"), ("2026-09-16", "expense", "Utilities", "2400", "Electricity and internet"),
        ("2026-09-22", "expense", "Healthcare", "1900", "Medicine"), ("2026-10-01", "income", "Salary", "65000", "October salary"),
        ("2026-10-02", "income", "Freelance", "12000", "Data analysis work"), ("2026-10-04", "expense", "Rent and Housing", "18000", "Monthly rent"),
        ("2026-10-08", "expense", "Groceries", "5750", "Household groceries"), ("2026-10-15", "expense", "Transportation", "3200", "Fuel and metro"),
        ("2026-10-19", "expense", "Entertainment", "1800", "Movie and subscription"), ("2026-10-25", "expense", "Utilities", "2500", "Electricity and internet")]
    for raw_date, kind, category, amount, description in samples:
        db.session.add(Transaction(transaction_date=date.fromisoformat(raw_date), kind=kind, category_id=by_name[category].id,
                                   amount=Decimal(amount), description=description, payment_method="UPI"))
    db.session.flush()
    for name, amount in (("Groceries", "5000"), ("Rent and Housing", "18000"), ("Transportation", "3500"), ("Utilities", "3000"), ("Entertainment", "2000")):
        db.session.add(MonthlyBudget(category_id=by_name[name].id, month=10, year=2026, amount=Decimal(amount)))
    db.session.commit(); return True
