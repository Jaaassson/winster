"""Flask application factory."""
import os
from flask import Flask

from app.config import get_config
from app.extensions import init_extensions, db


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: Configuration name (development/production/testing).
            Falls back to FLASK_ENV environment variable.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/static",
    )

    config_class = get_config(config_name)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    init_extensions(app)

    from app.middleware.error_handler import register_error_handlers

    register_error_handlers(app)

    from app.routes import register_blueprints

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health_check():
        return {"status": "ok", "message": "Server is running"}

    return app
