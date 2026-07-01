from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from datetime import datetime

from app.extensions import db
from app.models import Banner
from app.utils.response import success, error
from app.utils.i18n import get_lang, get_localized_value, get_i18n_field
import json

bp = Blueprint("banners", __name__, url_prefix="/api/v1")


def banner_to_dict(banner, lang=None):
    if lang is None:
        lang = get_lang()
    title_json = get_i18n_field(banner.title)
    button_text_json = get_i18n_field(banner.button_text)
    return {
        "id": banner.id,
        "image": banner.image_url,
        "image_url": banner.image_url,
        "title": get_localized_value(banner.title, lang),
        "title_i18n": title_json,
        "button_text": get_localized_value(banner.button_text, lang),
        "button_text_i18n": button_text_json,
        "link": banner.link_url or "",
        "link_url": banner.link_url,
        "sort_order": banner.sort_order,
        "status": banner.status,
        "is_online": banner.status == 1,
    }


@bp.route("/banners", methods=["GET"])
def get_banners():
    banners = Banner.query_active().filter_by(status=1).order_by(Banner.sort_order.asc()).all()
    data = [banner_to_dict(banner) for banner in banners]
    return success(data)


@bp.route("/admin/banners", methods=["GET"])
@jwt_required()
def admin_list_banners():
    banners = Banner.query_active().order_by(Banner.sort_order.asc()).all()
    data = []
    for banner in banners:
        title_json = get_i18n_field(banner.title)
        button_text_json = get_i18n_field(banner.button_text)
        data.append({
            "id": banner.id,
            "image_url": banner.image_url,
            "title": banner.title,
            "title_i18n": title_json,
            "button_text": banner.button_text,
            "button_text_i18n": button_text_json,
            "link_url": banner.link_url,
            "sort_order": banner.sort_order,
            "status": banner.status,
            "created_at": banner.created_at.isoformat() if banner.created_at else None,
            "updated_at": banner.updated_at.isoformat() if banner.updated_at else None,
        })
    return success(data)


@bp.route("/admin/banners", methods=["POST"])
@jwt_required()
def create_banner():
    data = request.get_json(silent=True) or {}
    image_url = data.get("image_url")
    if not image_url:
        return error("图片地址不能为空")

    title = data.get("title")
    title_json = json.dumps(title, ensure_ascii=False) if isinstance(title, dict) else title

    button_text = data.get("button_text")
    button_text_json = json.dumps(button_text, ensure_ascii=False) if isinstance(button_text, dict) else button_text

    banner = Banner(
        image_url=image_url,
        title=title_json,
        button_text=button_text_json,
        link_url=data.get("link_url"),
        sort_order=data.get("sort_order", 0),
        status=data.get("status", 1),
    )
    db.session.add(banner)
    db.session.commit()

    title_i18n = get_i18n_field(banner.title)
    button_text_i18n = get_i18n_field(banner.button_text)
    return success({
        "id": banner.id,
        "image_url": banner.image_url,
        "title": banner.title,
        "title_i18n": title_i18n,
        "button_text": banner.button_text,
        "button_text_i18n": button_text_i18n,
        "link_url": banner.link_url,
        "sort_order": banner.sort_order,
        "status": banner.status,
    }, "创建成功")


@bp.route("/admin/banners/<int:banner_id>", methods=["PUT"])
@jwt_required()
def update_banner(banner_id):
    banner = Banner.query_active().filter_by(id=banner_id).first()
    if not banner:
        return error("轮播图不存在", 404)

    data = request.get_json(silent=True) or {}

    if "image_url" in data:
        banner.image_url = data["image_url"]
    if "title" in data:
        title = data["title"]
        banner.title = json.dumps(title, ensure_ascii=False) if isinstance(title, dict) else title
    if "button_text" in data:
        button_text = data["button_text"]
        banner.button_text = json.dumps(button_text, ensure_ascii=False) if isinstance(button_text, dict) else button_text
    if "link_url" in data:
        banner.link_url = data["link_url"]
    if "sort_order" in data:
        banner.sort_order = data["sort_order"]
    if "status" in data:
        banner.status = data["status"]

    db.session.commit()

    title_i18n = get_i18n_field(banner.title)
    button_text_i18n = get_i18n_field(banner.button_text)
    return success({
        "id": banner.id,
        "image_url": banner.image_url,
        "title": banner.title,
        "title_i18n": title_i18n,
        "button_text": banner.button_text,
        "button_text_i18n": button_text_i18n,
        "link_url": banner.link_url,
        "sort_order": banner.sort_order,
        "status": banner.status,
    }, "更新成功")


@bp.route("/admin/banners/<int:banner_id>", methods=["DELETE"])
@jwt_required()
def delete_banner(banner_id):
    banner = Banner.query_active().filter_by(id=banner_id).first()
    if not banner:
        return error("轮播图不存在", 404)

    banner.deleted_at = datetime.utcnow()
    db.session.commit()

    return success(message="删除成功")
