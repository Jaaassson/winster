import json
from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Product, Category
from app.utils.response import success, error, success_paginated
from app.utils.pagination import paginate_query
from app.utils.i18n import get_lang, get_localized_value

products_bp = Blueprint("products", __name__, url_prefix="/api/v1")
admin_products_bp = Blueprint("admin_products", __name__, url_prefix="/api/v1/admin/products")


def parse_json_field(value):
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None
    return None


def product_to_dict(product, lang=None):
    if lang is None:
        lang = get_lang()

    name_json = parse_json_field(product.name)
    desc_json = parse_json_field(product.description)
    packaging_json = parse_json_field(product.packaging)
    images_json = parse_json_field(product.images)
    specs_json = parse_json_field(product.specs)

    return {
        "id": product.id,
        "category_id": product.category_id,
        "name": get_localized_value(name_json, lang),
        "name_i18n": name_json,
        "model": product.model,
        "description": get_localized_value(desc_json, lang),
        "description_i18n": desc_json,
        "images": images_json or [],
        "specs": specs_json or [],
        "price_usd": product.price_usd,
        "price_cny": product.price_cny,
        "stock": product.stock,
        "moq": product.moq,
        "packaging": get_localized_value(packaging_json, lang),
        "packaging_i18n": packaging_json,
        "sort_order": product.sort_order,
        "is_hot": product.is_hot,
        "status": product.status,
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "updated_at": product.updated_at.isoformat() if product.updated_at else None,
    }


@products_bp.get("/products")
def get_products():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    category_id = request.args.get("category_id", type=int)
    keyword = request.args.get("keyword", "").strip()
    sort_by = request.args.get("sort_by", "sort_order")
    order = request.args.get("order", "asc")

    query = Product.query_active().filter_by(status=1)

    if category_id:
        category_ids = get_category_and_children_ids(category_id)
        query = query.filter(Product.category_id.in_(category_ids))

    if keyword:
        query = query.filter(Product.name.like(f"%{keyword}%"))

    # 支持两种参数格式：
    # 1. sort_by=price_asc 或 sort_by=price_desc
    # 2. sort_by=price&order=asc 或 sort_by=price&order=desc
    sort_mapping = {
        "sort_order": Product.sort_order.asc(),
        "price_asc": Product.price_usd.asc(),
        "price_desc": Product.price_usd.desc(),
        "newest": Product.created_at.desc(),
    }

    # 如果 sort_by 包含 _asc 或 _desc，直接使用
    if sort_by in sort_mapping:
        order_clause = sort_mapping[sort_by]
    else:
        # 否则解析 sort_by + order 组合
        order = order.lower() if order else "asc"
        if sort_by == "price":
            order_clause = Product.price_usd.asc() if order == "asc" else Product.price_usd.desc()
        elif sort_by == "created_at":
            order_clause = Product.created_at.asc() if order == "asc" else Product.created_at.desc()
        else:
            order_clause = Product.sort_order.asc()

    query = query.order_by(order_clause)

    result = paginate_query(query, page=page, page_size=page_size)
    lang = get_lang()
    items = [product_to_dict(item, lang) for item in result["items"]]

    return success_paginated(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        message="Products retrieved successfully",
    )


def get_category_and_children_ids(category_id: int):
    """获取分类及其所有子分类的ID列表"""
    ids = [category_id]
    children = Category.query_active().filter_by(parent_id=category_id).all()
    for child in children:
        ids.extend(get_category_and_children_ids(child.id))
    return ids


@products_bp.get("/products/hot")
def get_hot_products():
    products = (
        Product.query_active()
        .filter_by(status=1, is_hot=1)
        .order_by(Product.sort_order.asc())
        .limit(8)
        .all()
    )
    lang = get_lang()
    data = [product_to_dict(p, lang) for p in products]
    return success(data=data, message="Hot products retrieved successfully")


@products_bp.get("/products/<int:id>")
def get_product_detail(id):
    product = Product.query_active().filter_by(id=id, status=1).first()
    if not product:
        return error(message="Product not found", code=404)

    lang = get_lang()
    data = product_to_dict(product, lang)
    return success(data=data, message="Product detail retrieved successfully")


@admin_products_bp.get("")
@jwt_required()
def admin_get_products():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    category_id = request.args.get("category_id", type=int)
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status", type=int)

    query = Product.query_active()

    if category_id:
        query = query.filter_by(category_id=category_id)

    if keyword:
        query = query.filter(Product.name.like(f"%{keyword}%"))

    if status is not None:
        query = query.filter_by(status=status)

    query = query.order_by(Product.created_at.desc())

    result = paginate_query(query, page=page, page_size=page_size)
    lang = get_lang()
    items = [product_to_dict(item, lang) for item in result["items"]]

    return success_paginated(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        message="Products retrieved successfully",
    )


@admin_products_bp.post("")
@jwt_required()
def admin_create_product():
    data = request.get_json()
    if not data:
        return error(message="Invalid request data", code=400)

    category_id = data.get("category_id")
    name = data.get("name")
    model = data.get("model")
    description = data.get("description")
    images = data.get("images")
    specs = data.get("specs")
    price_usd = data.get("price_usd", 0)
    price_cny = data.get("price_cny", 0)
    stock = data.get("stock", 0)
    moq = data.get("moq", 1)
    packaging = data.get("packaging")
    sort_order = data.get("sort_order", 0)
    is_hot = data.get("is_hot", 0)
    status = data.get("status", 1)

    if not category_id or not name:
        return error(message="Category and name are required", code=400)

    category = Category.query_active().filter_by(id=category_id).first()
    if not category:
        return error(message="Category not found", code=404)

    name_json = json.dumps(name, ensure_ascii=False) if isinstance(name, dict) else name
    desc_json = json.dumps(description, ensure_ascii=False) if isinstance(description, dict) else description
    packaging_json = json.dumps(packaging, ensure_ascii=False) if isinstance(packaging, dict) else packaging
    images_json = json.dumps(images, ensure_ascii=False) if isinstance(images, (list, dict)) else images
    specs_json = json.dumps(specs, ensure_ascii=False) if isinstance(specs, (list, dict)) else specs

    product = Product(
        category_id=category_id,
        name=name_json,
        model=model,
        description=desc_json,
        images=images_json,
        specs=specs_json,
        price_usd=price_usd,
        price_cny=price_cny,
        stock=stock,
        moq=moq,
        packaging=packaging_json,
        sort_order=sort_order,
        is_hot=is_hot,
        status=status,
    )

    db.session.add(product)
    db.session.commit()

    lang = get_lang()
    data = product_to_dict(product, lang)
    return success(data=data, message="Product created successfully")


@admin_products_bp.put("/<int:id>")
@jwt_required()
def admin_update_product(id):
    product = Product.query_active().filter_by(id=id).first()
    if not product:
        return error(message="Product not found", code=404)

    data = request.get_json()
    if not data:
        return error(message="Invalid request data", code=400)

    if "category_id" in data:
        category_id = data["category_id"]
        category = Category.query_active().filter_by(id=category_id).first()
        if not category:
            return error(message="Category not found", code=404)
        product.category_id = category_id

    if "name" in data:
        name = data["name"]
        product.name = json.dumps(name, ensure_ascii=False) if isinstance(name, dict) else name

    if "model" in data:
        product.model = data["model"]

    if "description" in data:
        description = data["description"]
        product.description = json.dumps(description, ensure_ascii=False) if isinstance(description, dict) else description

    if "images" in data:
        images = data["images"]
        product.images = json.dumps(images, ensure_ascii=False) if isinstance(images, (list, dict)) else images

    if "specs" in data:
        specs = data["specs"]
        product.specs = json.dumps(specs, ensure_ascii=False) if isinstance(specs, (list, dict)) else specs

    if "price_usd" in data:
        product.price_usd = data["price_usd"]

    if "price_cny" in data:
        product.price_cny = data["price_cny"]

    if "stock" in data:
        product.stock = data["stock"]

    if "moq" in data:
        product.moq = data["moq"]

    if "packaging" in data:
        packaging = data["packaging"]
        product.packaging = json.dumps(packaging, ensure_ascii=False) if isinstance(packaging, dict) else packaging

    if "sort_order" in data:
        product.sort_order = data["sort_order"]

    if "is_hot" in data:
        product.is_hot = data["is_hot"]

    if "status" in data:
        product.status = data["status"]

    db.session.commit()

    lang = get_lang()
    data = product_to_dict(product, lang)
    return success(data=data, message="Product updated successfully")


@admin_products_bp.delete("/<int:id>")
@jwt_required()
def admin_delete_product(id):
    product = Product.query_active().filter_by(id=id).first()
    if not product:
        return error(message="Product not found", code=404)

    product.deleted_at = datetime.utcnow()
    db.session.commit()

    return success(message="Product deleted successfully")


@admin_products_bp.patch("/<int:id>/status")
@jwt_required()
def admin_toggle_product_status(id):
    product = Product.query_active().filter_by(id=id).first()
    if not product:
        return error(message="Product not found", code=404)

    product.status = 0 if product.status == 1 else 1
    db.session.commit()

    lang = get_lang()
    data = product_to_dict(product, lang)
    return success(data=data, message="Product status updated successfully")
