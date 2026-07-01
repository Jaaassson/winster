"""Application configuration classes."""
import os
from typing import List


class Config:
    """Base configuration class."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret-key")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "./app/static/uploads")
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))

    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:5175").split(",")

    ALLOWED_IMAGE_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif", "webp"}

    DEFAULT_LANGUAGE: str = "zh"
    SUPPORTED_LANGUAGES: List[str] = ["zh", "en"]


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG: bool = True
    TESTING: bool = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG: bool = False
    TESTING: bool = False


class TestingConfig(Config):
    """Testing configuration."""

    DEBUG: bool = True
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


config_by_name: dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(config_name: str | None = None) -> type[Config]:
    """Get configuration class by name.

    Args:
        config_name: Configuration name (development/production/testing).
            Falls back to FLASK_ENV environment variable.

    Returns:
        Configuration class.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(config_name, DevelopmentConfig)
