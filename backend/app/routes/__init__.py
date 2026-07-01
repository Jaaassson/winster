from flask import Flask

from app.routes.auth import auth_bp
from app.routes.products import products_bp, admin_products_bp
from app.routes.categories import bp as categories_bp
from app.routes.inquiries import bp as inquiries_bp
from app.routes.news import bp as news_bp
from app.routes.banners import bp as banners_bp
from app.routes.site_config import bp as site_config_bp
from app.routes.upload import bp as upload_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(admin_products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(inquiries_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(banners_bp)
    app.register_blueprint(site_config_bp)
    app.register_blueprint(upload_bp)


__all__ = ["register_blueprints"]
