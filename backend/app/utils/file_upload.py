"""文件上传工具。"""
import os
import uuid
from flask import current_app, url_for
from werkzeug.utils import secure_filename
from typing import Optional

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许。

    Args:
        filename: 文件名

    Returns:
        是否允许
    """
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_random_filename(original_filename: str) -> str:
    """生成随机文件名。

    Args:
        original_filename: 原始文件名

    Returns:
        随机文件名（保留扩展名）
    """
    ext = original_filename.rsplit(".", 1)[1].lower() if "." in original_filename else "jpg"
    return f"{uuid.uuid4().hex}.{ext}"


def save_image(file_storage) -> tuple:
    """保存上传的图片。

    Args:
        file_storage: Flask 的 FileStorage 对象

    Returns:
        (url, error) 元组，成功时 url 为路径，error 为 None；失败时 url 为 None，error 为错误信息
    """
    if not file_storage or file_storage.filename == "":
        return None, "未选择文件"

    if not allowed_file(file_storage.filename):
        return None, "不支持的文件类型"

    filename = generate_random_filename(file_storage.filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    file_storage.save(filepath)

    return f"/static/uploads/{filename}", None
