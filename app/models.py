from datetime import datetime
from decimal import Decimal
from .extensions import db


class Category(db.Model):
    __tablename__ = "categories"
    __table_args__ = (db.UniqueConstraint("name", "kind", name="uq_category_name_kind"),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    kind = db.Column(db.String(10), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    transactions = db.relationship("Transaction", back_populates="category", lazy="select")
    budgets = db.relationship("MonthlyBudget", back_populates="category", lazy="select")

    def as_dict(self):
        return {"id": self.id, "name": self.name, "type": self.kind}


class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = (db.Index("ix_transactions_date_kind", "transaction_date", "kind"),)
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False, index=True)
    kind = db.Column(db.String(10), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = db.relationship("Category", back_populates="transactions")

    def as_dict(self):
        return {"id": self.id, "date": self.transaction_date.isoformat(), "type": self.kind,
                "category": self.category.name, "category_id": self.category_id,
                "amount": str(self.amount), "description": self.description,
                "payment_method": self.payment_method, "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()}


class MonthlyBudget(db.Model):
    __tablename__ = "monthly_budgets"
    __table_args__ = (db.UniqueConstraint("category_id", "month", "year", name="uq_budget_category_month_year"),)
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = db.relationship("Category", back_populates="budgets")

    def as_dict(self):
        return {"id": self.id, "category": self.category.name, "category_id": self.category_id,
                "month": self.month, "year": self.year, "amount": str(self.amount)}
