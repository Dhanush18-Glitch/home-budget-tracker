import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def database_url():
    """Return a SQLAlchemy-compatible URL from common cloud database URLs."""
    value = os.getenv("DATABASE_URL", "").strip()
    if value.startswith("mysql://"):
        return "mysql+pymysql://" + value[len("mysql://"):]
    if value.startswith("postgres://"):
        return "postgresql+psycopg://" + value[len("postgres://"):]
    if value.startswith("postgresql://"):
        return "postgresql+psycopg://" + value[len("postgresql://"):]
    return value or f"sqlite:///{BASE_DIR / 'instance' / 'home_budget.db'}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

