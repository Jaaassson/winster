from flask import Blueprint, request
from flask_jwt_extended import jwt_required
import json

from app.extensions import db
from app.models import SiteConfig
from app.utils.response import success, error
from app.utils.i18n import get_i18n_field

bp = Blueprint("site_config", __name__, url_prefix="/api/v1")


def _config_to_dict(config, admin=False):
    data = {
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
    if admin:
        data["company_name_i18n"] = get_i18n_field(config.company_name)
    return data


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
    return success(_config_to_dict(config, admin=True))


@bp.route("/admin/site-config", methods=["PUT"])
@jwt_required()
def update_site_config():
    config = get_or_create_config()
    data = request.get_json(silent=True) or {}

    i18n_fields = ["site_name", "site_title", "keywords", "description", "company_name", "address", "about_us"]
    normal_fields = ["phone", "email", "facebook", "twitter", "linkedin", "instagram"]

    for field in i18n_fields:
        if field in data:
            value = data[field]
            if isinstance(value, dict):
                setattr(config, field, json.dumps(value, ensure_ascii=False))
            else:
                setattr(config, field, value)

    for field in normal_fields:
        if field in data:
            setattr(config, field, data[field])

    db.session.commit()

    return success(_config_to_dict(config, admin=True), "更新成功")
