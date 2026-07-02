import logging
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required

from app.utils.file_upload import save_image, allowed_file
from app.utils.response import success, error

logger = logging.getLogger(__name__)

bp = Blueprint("upload", __name__, url_prefix="/api/v1/admin")


@bp.route("/upload/image", methods=["POST"])
@jwt_required()
def upload_image():
    logger.info(f"=== Upload request received ===")
    logger.info(f"Content-Type: {request.content_type}")
    logger.info(f"Content-Length: {request.content_length}")
    logger.info(f"Files in request: {list(request.files.keys())}")
    logger.info(f"Form fields: {list(request.form.keys())}")

    if "file" not in request.files:
        logger.error("File field not found in request")
        return error("未找到文件字段")

    file = request.files["file"]
    logger.info(f"File found: {file.filename}")

    if file.filename == "":
        logger.error("File name is empty")
        return error("未选择文件")

    if not allowed_file(file.filename):
        allowed = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", {"jpg", "jpeg", "png", "gif", "webp"})
        logger.error(f"File type not allowed: {file.filename}")
        return error(f"不支持的文件类型，仅支持: {', '.join(allowed)}")

    file_url, err = save_image(file)
    if err:
        logger.error(f"Save image error: {err}")
        return error(err)

    logger.info(f"Upload success: {file_url}")
    return success({"url": file_url}, "上传成功")
