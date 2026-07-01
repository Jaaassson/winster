"""Flask extensions initialization."""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def query_active(cls):
        return cls.query.filter_by(deleted_at=None)


def init_extensions(app) -> None:
    """Initialize Flask extensions with the application instance.

    Args:
        app: Flask application instance.
    """
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
