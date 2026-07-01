from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import SiteConfig
from app.utils.response import success, error

bp = Blueprint("site_config", __name__, url_prefix="/api/v1")


def _config_to_dict(config):
    return {
        "id": config.id,
        "site_name": config.site_name,
        "site_title": config.site_title,
        "keywords": config.keywords,
        "description": config.description,
        "company_name": config.company_name,
        "phone": config.phone,
        "email": config.email,
        "address": config.address,
        "about_us": config.about_us,
        "facebook": config.facebook,
        "twitter": config.twitter,
        "linkedin": config.linkedin,
        "instagram": config.instagram,
        "created_at": config.created_at.isoformat() if config.created_at else None,
        "updated_at": config.updated_at.isoformat() if config.updated_at else None,
    }


def get_or_create_config():
    config = SiteConfig.query.filter_by(id=1).first()
    if not config:
        config = SiteConfig(id=1)
        db.session.add(config)
        db.session.commit()
    return config


@bp.route("/site-config", methods=["GET"])
def get_site_config():
    config = get_or_create_config()
    return success(_config_to_dict(config))


@bp.route("/admin/site-config", methods=["GET"])
@jwt_required()
def admin_get_site_config():
    config = get_or_create_config()
    return success(_config_to_dict(config))


@bp.route("/admin/site-config", methods=["PUT"])
@jwt_required()
def update_site_config():
    config = get_or_create_config()
    data = request.get_json(silent=True) or {}

    fields = [
        "site_name", "site_title", "keywords", "description",
        "company_name", "phone", "email", "address", "about_us",
        "facebook", "twitter", "linkedin", "instagram",
    ]

    for field in fields:
        if field in data:
            setattr(config, field, data[field])

    db.session.commit()

    return success(_config_to_dict(config), "更新成功")
