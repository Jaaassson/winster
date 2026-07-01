from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Admin
from app.utils.response import success, error
from app.utils.i18n import get_lang

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json()
    if not data:
        return error(message="Invalid request data", code=400)

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error(message="Username and password are required", code=400)

    admin = Admin.query_active().filter_by(username=username).first()
    if not admin:
        return error(message="Invalid username or password", code=401)

    if admin.status != 1:
        return error(message="Account is disabled", code=403)

    if not admin.check_password(password):
        return error(message="Invalid username or password", code=401)

    access_token = create_access_token(identity=str(admin.id))

    user_data = {
        "id": admin.id,
        "username": admin.username,
        "nickname": admin.nickname,
        "avatar": admin.avatar,
    }

    return success(
        data={
            "access_token": access_token,
            "user": user_data,
        },
        message="Login successful",
    )


@auth_bp.post("/refresh")
@jwt_required()
def refresh():
    current_user_id = get_jwt_identity()
    admin = Admin.query_active().filter_by(id=current_user_id).first()
    if not admin:
        return error(message="User not found", code=404)

    new_token = create_access_token(identity=str(admin.id))

    user_data = {
        "id": admin.id,
        "username": admin.username,
        "nickname": admin.nickname,
        "avatar": admin.avatar,
    }

    return success(
        data={
            "access_token": new_token,
            "user": user_data,
        },
        message="Token refreshed successfully",
    )


@auth_bp.get("/me")
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    admin = Admin.query_active().filter_by(id=current_user_id).first()
    if not admin:
        return error(message="User not found", code=404)

    user_data = {
        "id": admin.id,
        "username": admin.username,
        "nickname": admin.nickname,
        "avatar": admin.avatar,
        "status": admin.status,
        "created_at": admin.created_at.isoformat() if admin.created_at else None,
    }

    return success(data=user_data, message="User info retrieved successfully")
