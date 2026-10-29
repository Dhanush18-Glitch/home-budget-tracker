import pytest
from app import create_app
from app.extensions import db
from app.services.seed import seed_defaults


@pytest.fixture()
def app(tmp_path):
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False, "SECRET_KEY": "test", "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}"})
    with app.app_context():
        db.create_all(); seed_defaults()
    yield app
    with app.app_context(): db.session.remove(); db.drop_all()


@pytest.fixture()
def client(app):
    with app.app_context():
        yield app.test_client()
