import os
from dotenv import load_dotenv

load_dotenv()


def _bool(v, default=False):
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes", "on")


class Config:
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = _bool(os.getenv("FLASK_DEBUG"), ENV == "development")
    PORT = int(os.getenv("PORT", "5000"))

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_NAME = os.getenv("DB_NAME", "winster")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 1800, "pool_pre_ping": True}

    JWT_SECRET = os.getenv("JWT_SECRET", "winster-secret")
    JWT_EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", "7"))

    UPLOAD_DIR = os.path.abspath(os.getenv("UPLOAD_DIR", "./uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "5242880"))

    CORS_ORIGIN = [
        x.strip() for x in os.getenv("CORS_ORIGIN", "").split(",") if x.strip()
    ] or ["*"]