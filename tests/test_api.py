from app.extensions import db
from app.models import Category, Transaction


def income_category(): return Category.query.filter_by(kind="income").first().id
def expense_category(): return Category.query.filter_by(kind="expense").first().id


def test_health_and_default_categories(client):
    assert client.get("/api/health").status_code == 200
    assert len(client.get("/api/categories").get_json()) == 18


def test_transaction_crud_and_filtered_totals(client):
    payload = {"date": "2026-10-02", "type": "income", "category_id": income_category(), "amount": "1000.50", "description": "Test salary"}
    created = client.post("/api/transactions", json=payload); assert created.status_code == 201
    item = created.get_json(); assert item["amount"] == "1000.50"
    result = client.get("/api/transactions?type=income").get_json(); assert result["totals"]["income"] == "1000.50"
    payload.update({"amount": "900.00", "description": "Updated salary"}); assert client.put(f"/api/transactions/{item['id']}", json=payload).status_code == 200
    assert client.delete(f"/api/transactions/{item['id']}").status_code == 204
    assert client.get(f"/api/transactions/{item['id']}").status_code == 404


def test_invalid_transaction_and_matching_category_required(client):
    bad = {"date": "not-a-date", "type": "income", "category_id": expense_category(), "amount": "0", "description": "x"}
    response = client.post("/api/transactions", json=bad)
    assert response.status_code == 400


def test_budget_duplicate_and_overspending(client):
    expense = expense_category()
    transaction = {"date": "2026-10-05", "type": "expense", "category_id": expense, "amount": "150.00", "description": "Groceries"}
    assert client.post("/api/transactions", json=transaction).status_code == 201
    budget = {"category_id": expense, "month": 10, "year": 2026, "amount": "100.00"}
    assert client.post("/api/budgets", json=budget).status_code == 201
    assert client.post("/api/budgets", json=budget).status_code == 409
    data = client.get("/api/analytics/budgets?year=2026&month=10").get_json()
    assert data[0]["status"] == "over" and data[0]["utilization"] == 150.0


def test_csv_formula_injection_is_escaped(client):
    payload = {"date": "2026-10-05", "type": "income", "category_id": income_category(), "amount": "1", "description": "=SUM(A1:A2)"}
    assert client.post("/api/transactions", json=payload).status_code == 201
    body = client.get("/api/exports/transactions.csv").get_data(as_text=True)
    assert "'=SUM(A1:A2)" in body


def test_report_exports_and_filtered_transactions(client):
    expense = {"date": "2026-10-05", "type": "expense", "category_id": expense_category(), "amount": "25", "description": "Filtered purchase"}
    income = {"date": "2026-10-05", "type": "income", "category_id": income_category(), "amount": "50", "description": "Other record"}
    assert client.post("/api/transactions", json=expense).status_code == 201
    assert client.post("/api/transactions", json=income).status_code == 201
    filtered = client.get("/api/exports/transactions.csv?type=expense").get_data(as_text=True)
    assert "Filtered purchase" in filtered and "Other record" not in filtered
    assert client.get("/api/exports/monthly-summary.csv").status_code == 200
    assert client.get("/api/exports/categories.csv?year=2026&month=10").status_code == 200


def test_charts_and_empty_metrics(client):
    dashboard = client.get("/api/dashboard?year=2020&month=1").get_json()
    assert dashboard["income"] == "0.00" and dashboard["savings_rate"] == 0.0
    response = client.post("/api/charts?year=2020&month=1")
    assert response.status_code == 201 and len(response.get_json()) == 4


def test_dashboard_date_filter_and_chart_route(client):
    payload = {"date": "2026-10-20", "type": "income", "category_id": income_category(), "amount": "100.00", "description": "Date filter income"}
    assert client.post("/api/transactions", json=payload).status_code == 201
    dashboard = client.get("/api/dashboard?date=2026-10-19").get_json()
    assert dashboard["income"] == "0.00" and dashboard["period"]["as_of"] == "2026-10-19"
    page = client.get("/?date=2026-10-20")
    assert page.status_code == 200 and b"Live charts" in page.data
    assert b"dashboard_expense_distribution.png?v=" in page.data
    assert client.get("/charts/dashboard_expense_distribution.png").status_code == 200
