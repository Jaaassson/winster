from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required

from app.utils.file_upload import save_image, allowed_file
from app.utils.response import success, error

bp = Blueprint("upload", __name__, url_prefix="/api/v1/admin")


@bp.route("/upload/image", methods=["POST"])
@jwt_required()
def upload_image():
    if "file" not in request.files:
        return error("未找到文件字段")

    file = request.files["file"]
    if file.filename == "":
        return error("未选择文件")

    if not allowed_file(file.filename):
        allowed = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", {"jpg", "jpeg", "png", "gif", "webp"})
        return error(f"不支持的文件类型，仅支持: {', '.join(allowed)}")

    file_url, err = save_image(file)
    if err:
        return error(err)

    return success({"url": file_url}, "上传成功")
