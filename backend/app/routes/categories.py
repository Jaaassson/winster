import json
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Category
from app.utils.response import success, error
from app.utils.i18n import get_lang, get_localized_value, get_i18n_field

bp = Blueprint("categories", __name__, url_prefix="/api/v1")


def category_to_dict(cat, lang=None):
    if lang is None:
        lang = get_lang()
    name_json = get_i18n_field(cat.name)
    return {
        "id": cat.id,
        "name": get_localized_value(cat.name, lang),
        "name_i18n": name_json,
        "image": cat.image,
        "parent_id": cat.parent_id,
        "sort_order": cat.sort_order,
        "status": cat.status,
        "created_at": cat.created_at.isoformat() if cat.created_at else None,
        "updated_at": cat.updated_at.isoformat() if cat.updated_at else None,
    }


def build_tree(categories, parent_id=0, lang=None):
    tree = []
    for cat in categories:
        if cat.parent_id == parent_id:
            children = build_tree(categories, cat.id, lang)
            cat_dict = category_to_dict(cat, lang)
            cat_dict["children"] = children
            tree.append(cat_dict)
    tree.sort(key=lambda x: (x["sort_order"], x["id"]))
    return tree


@bp.route("/categories", methods=["GET"])
def list_categories():
    lang = get_lang()
    categories = Category.query_active().filter_by(status=1).all()
    tree = build_tree(categories, 0, lang)
    return success(tree)


@bp.route("/admin/categories", methods=["GET"])
@jwt_required()
def admin_list_categories():
    lang = get_lang()
    categories = Category.query_active().all()
    tree = build_tree(categories, 0, lang)
    return success(tree)


@bp.route("/admin/categories", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return error("分类名称不能为空")
    category = Category()
    category.name = json.dumps(name, ensure_ascii=False) if isinstance(name, dict) else name
    category.image = data.get("image")
    category.parent_id = data.get("parent_id", 0)
    category.sort_order = data.get("sort_order", 0)
    category.status = data.get("status", 1)
    db.session.add(category)
    db.session.commit()
    return success(category_to_dict(category), "创建成功")


@bp.route("/admin/categories/<int:id>", methods=["PUT"])
@jwt_required()
def update_category(id):
    category = Category.query_active().filter_by(id=id).first()
    if not category:
        return error("分类不存在", 404)
    data = request.get_json(silent=True) or {}
    if "name" in data:
        name = data["name"]
        category.name = json.dumps(name, ensure_ascii=False) if isinstance(name, dict) else name
    if "image" in data:
        category.image = data["image"]
    if "parent_id" in data:
        category.parent_id = data["parent_id"]
    if "sort_order" in data:
        category.sort_order = data["sort_order"]
    if "status" in data:
        category.status = data["status"]
    db.session.commit()
    return success(category_to_dict(category), "更新成功")


@bp.route("/admin/categories/<int:id>/status", methods=["PATCH"])
@jwt_required()
def toggle_category_status(id):
    category = Category.query_active().filter_by(id=id).first()
    if not category:
        return error("分类不存在", 404)
    category.status = 0 if category.status == 1 else 1
    db.session.commit()
    return success(category_to_dict(category), "状态更新成功")


@bp.route("/admin/categories/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_category(id):
    category = Category.query_active().filter_by(id=id).first()
    if not category:
        return error("分类不存在", 404)
    from datetime import datetime
    category.deleted_at = datetime.utcnow()
    db.session.commit()
    return success(None, "删除成功")
