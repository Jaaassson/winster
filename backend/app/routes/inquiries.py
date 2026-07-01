import csv
import re
from io import StringIO
from datetime import datetime
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Inquiry
from app.utils.response import success, error, success_paginated
from app.utils.pagination import paginate_query
from app.utils.i18n import get_lang

bp = Blueprint("inquiries", __name__, url_prefix="/api/v1")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def inquiry_to_dict(inquiry):
    return {
        "id": inquiry.id,
        "customer_name": inquiry.customer_name,
        "email": inquiry.email,
        "country": inquiry.country,
        "quantity": inquiry.quantity,
        "message": inquiry.message,
        "product_id": inquiry.product_id,
        "is_read": inquiry.is_read,
        "is_replied": inquiry.is_replied,
        "replied_at": inquiry.replied_at.isoformat() if inquiry.replied_at else None,
        "created_at": inquiry.created_at.isoformat() if inquiry.created_at else None,
        "updated_at": inquiry.updated_at.isoformat() if inquiry.updated_at else None,
    }


@bp.route("/inquiries", methods=["POST"])
def submit_inquiry():
    data = request.get_json(silent=True) or {}
    customer_name = (data.get("customer_name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not customer_name:
        return error("客户姓名不能为空")
    if not email:
        return error("邮箱不能为空")
    if not EMAIL_RE.match(email):
        return error("邮箱格式不正确")
    if not message:
        return error("留言内容不能为空")

    inquiry = Inquiry()
    inquiry.customer_name = customer_name
    inquiry.email = email
    inquiry.message = message
    inquiry.country = data.get("country")
    inquiry.quantity = data.get("quantity")
    inquiry.product_id = data.get("product_id")
    inquiry.is_read = 0
    inquiry.is_replied = 0

    db.session.add(inquiry)
    db.session.commit()
    return success(inquiry_to_dict(inquiry), "提交成功")


@bp.route("/admin/inquiries", methods=["GET"])
@jwt_required()
def admin_list_inquiries():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    query = Inquiry.query_active()

    is_read = request.args.get("is_read")
    if is_read in ("0", "1"):
        query = query.filter(Inquiry.is_read == int(is_read))

    is_replied = request.args.get("is_replied")
    if is_replied in ("0", "1"):
        query = query.filter(Inquiry.is_replied == int(is_replied))

    country = request.args.get("country")
    if country:
        query = query.filter(Inquiry.country == country)

    keyword = (request.args.get("keyword") or "").strip()
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            (Inquiry.customer_name.like(like)) |
            (Inquiry.email.like(like)) |
            (Inquiry.message.like(like))
        )

    query = query.order_by(Inquiry.id.desc())

    result = paginate_query(query, page, page_size)
    items = [inquiry_to_dict(item) for item in result["items"]]

    return success_paginated(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@bp.route("/admin/inquiries/<int:id>", methods=["GET"])
@jwt_required()
def get_inquiry_detail(id):
    inquiry = Inquiry.query_active().filter_by(id=id).first()
    if not inquiry:
        return error("询盘不存在", 404)

    if inquiry.is_read == 0:
        inquiry.is_read = 1
        db.session.commit()

    return success(inquiry_to_dict(inquiry))


@bp.route("/admin/inquiries/<int:id>/status", methods=["PATCH"])
@jwt_required()
def mark_replied(id):
    inquiry = Inquiry.query_active().filter_by(id=id).first()
    if not inquiry:
        return error("询盘不存在", 404)

    inquiry.is_replied = 1
    inquiry.replied_at = datetime.utcnow()
    db.session.commit()

    return success(inquiry_to_dict(inquiry), "标记已回复成功")


@bp.route("/admin/inquiries/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_inquiry(id):
    inquiry = Inquiry.query_active().filter_by(id=id).first()
    if not inquiry:
        return error("询盘不存在", 404)

    inquiry.deleted_at = datetime.utcnow()
    db.session.commit()
    return success(None, "删除成功")


@bp.route("/admin/inquiries/export", methods=["GET"])
@jwt_required()
def export_inquiries():
    query = Inquiry.query_active()

    is_read = request.args.get("is_read")
    if is_read in ("0", "1"):
        query = query.filter(Inquiry.is_read == int(is_read))

    is_replied = request.args.get("is_replied")
    if is_replied in ("0", "1"):
        query = query.filter(Inquiry.is_replied == int(is_replied))

    country = request.args.get("country")
    if country:
        query = query.filter(Inquiry.country == country)

    keyword = (request.args.get("keyword") or "").strip()
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            (Inquiry.customer_name.like(like)) |
            (Inquiry.email.like(like)) |
            (Inquiry.message.like(like))
        )

    inquiries = query.order_by(Inquiry.id.desc()).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "客户姓名", "邮箱", "国家", "数量", "产品ID",
        "留言内容", "是否已读", "是否已回复", "回复时间", "创建时间"
    ])

    for inquiry in inquiries:
        writer.writerow([
            inquiry.id,
            inquiry.customer_name or "",
            inquiry.email or "",
            inquiry.country or "",
            inquiry.quantity or "",
            inquiry.product_id or "",
            (inquiry.message or "").replace("\n", " "),
            "是" if inquiry.is_read else "否",
            "是" if inquiry.is_replied else "否",
            inquiry.replied_at.strftime("%Y-%m-%d %H:%M:%S") if inquiry.replied_at else "",
            inquiry.created_at.strftime("%Y-%m-%d %H:%M:%S") if inquiry.created_at else "",
        ])

    output.seek(0)
    filename = f"inquiries_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/csv; charset=utf-8",
        }
    )
