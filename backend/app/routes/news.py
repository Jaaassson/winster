from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import News
from app.utils.response import success, error, success_paginated
from app.utils.pagination import paginate_query
from app.utils.i18n import get_lang

bp = Blueprint("news", __name__, url_prefix="/api/v1")


def news_to_dict(news):
    return {
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "cover_image": news.cover_image,
        "sort_order": news.sort_order,
        "status": news.status,
        "created_at": news.created_at.isoformat() if news.created_at else None,
        "updated_at": news.updated_at.isoformat() if news.updated_at else None,
    }


@bp.route("/news", methods=["GET"])
def list_news():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    query = News.query_active().filter_by(status=1)

    keyword = (request.args.get("keyword") or "").strip()
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(News.title.like(like))

    query = query.order_by(News.sort_order.asc(), News.id.desc())

    result = paginate_query(query, page, page_size)
    items = [news_to_dict(item) for item in result["items"]]

    return success_paginated(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@bp.route("/news/<int:id>", methods=["GET"])
def get_news_detail(id):
    news = News.query_active().filter_by(id=id, status=1).first()
    if not news:
        return error("新闻不存在", 404)
    return success(news_to_dict(news))


@bp.route("/admin/news", methods=["GET"])
@jwt_required()
def admin_list_news():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    query = News.query_active()

    status = request.args.get("status")
    if status in ("0", "1"):
        query = query.filter(News.status == int(status))

    keyword = (request.args.get("keyword") or "").strip()
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(News.title.like(like))

    query = query.order_by(News.sort_order.asc(), News.id.desc())

    result = paginate_query(query, page, page_size)
    items = [news_to_dict(item) for item in result["items"]]

    return success_paginated(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@bp.route("/admin/news", methods=["POST"])
@jwt_required()
def create_news():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return error("新闻标题不能为空")

    news = News()
    news.title = title
    news.content = data.get("content", "")
    news.cover_image = data.get("cover_image", "")
    news.sort_order = data.get("sort_order", 0)
    news.status = data.get("status", 1)

    db.session.add(news)
    db.session.commit()
    return success(news_to_dict(news), "创建成功")


@bp.route("/admin/news/<int:id>", methods=["PUT"])
@jwt_required()
def update_news(id):
    news = News.query_active().filter_by(id=id).first()
    if not news:
        return error("新闻不存在", 404)

    data = request.get_json(silent=True) or {}
    if "title" in data:
        news.title = data["title"]
    if "content" in data:
        news.content = data["content"]
    if "cover_image" in data:
        news.cover_image = data["cover_image"]
    if "sort_order" in data:
        news.sort_order = data["sort_order"]
    if "status" in data:
        news.status = data["status"]

    db.session.commit()
    return success(news_to_dict(news), "更新成功")


@bp.route("/admin/news/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_news(id):
    news = News.query_active().filter_by(id=id).first()
    if not news:
        return error("新闻不存在", 404)

    news.deleted_at = datetime.utcnow()
    db.session.commit()
    return success(None, "删除成功")
