# Migration notes

`20261029_0001_initial_schema.py` is the reproducible initial Alembic migration for the SQLAlchemy models. In a configured MySQL environment, initialize Flask-Migrate once with `flask --app manage:app db init` only if the `migrations` environment has not been created, then apply `flask --app manage:app db upgrade`. For the local SQLite demonstration path, `python manage.py init-db` creates the equivalent schema safely without dropping existing tables.
