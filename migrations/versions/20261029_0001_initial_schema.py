"""Initial Home Budget schema.

Revision ID: 20261029_0001
Revises:
Create Date: 2026-10-29
"""
from alembic import op
import sqlalchemy as sa

revision = "20261029_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("categories", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(80), nullable=False), sa.Column("kind", sa.String(10), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.UniqueConstraint("name", "kind", name="uq_category_name_kind"))
    op.create_index("ix_categories_kind", "categories", ["kind"])
    op.create_table("transactions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("transaction_date", sa.Date(), nullable=False), sa.Column("kind", sa.String(10), nullable=False), sa.Column("category_id", sa.Integer(), nullable=False), sa.Column("amount", sa.Numeric(12,2), nullable=False), sa.Column("description", sa.String(255), nullable=False), sa.Column("payment_method", sa.String(50)), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="RESTRICT"))
    op.create_index("ix_transactions_date_kind", "transactions", ["transaction_date", "kind"])
    op.create_table("monthly_budgets", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("category_id", sa.Integer(), nullable=False), sa.Column("month", sa.Integer(), nullable=False), sa.Column("year", sa.Integer(), nullable=False), sa.Column("amount", sa.Numeric(12,2), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="RESTRICT"), sa.UniqueConstraint("category_id", "month", "year", name="uq_budget_category_month_year"))


def downgrade():
    op.drop_table("monthly_budgets"); op.drop_table("transactions"); op.drop_table("categories")
