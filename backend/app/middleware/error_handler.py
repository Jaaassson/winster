"""全局异常处理中间件。"""
import logging
import traceback
from flask import Flask
from app.utils.response import error

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """注册全局错误处理器。

    Args:
        app: Flask 应用实例
    """

    @app.errorhandler(400)
    def bad_request(e):
        return error("Bad Request", 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error("Unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error("Forbidden", 403)

    @app.errorhandler(404)
    def not_found(e):
        return error("Not Found", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error("Method Not Allowed", 405)

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.exception("Internal Server Error: %s", str(e))
        traceback.print_exc()
        return error("Internal Server Error", 500)

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Unhandled Exception: %s", str(e))
        traceback.print_exc()
        return error(str(e), 500)
