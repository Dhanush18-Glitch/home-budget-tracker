import os
from pathlib import Path
from flask import Flask, jsonify
from config import Config
from .extensions import db, migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    # Vercel's deployed application bundle is read-only.  Creating Flask's
    # local ``instance`` directory there makes the function fail while it is
    # importing, before it can connect to the configured hosted database.
    # Local development and tests still use the normal writable instance path.
    if not os.getenv("VERCEL"):
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.web import web_bp
    from .routes.api import api_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.errorhandler(404)
    def missing(_error):
        if os.getenv("REQUESTED_WITH") == "api":
            return jsonify(error={"code": "not_found", "message": "Resource not found."}), 404
        return app.jinja_env.get_template("404.html").render(), 404

    @app.errorhandler(500)
    def server_error(_error):
        app.logger.exception("Unhandled server error")
        return jsonify(error={"code": "server_error", "message": "An unexpected error occurred."}), 500

    return app

