"""统一响应格式工具。"""
from flask import jsonify
from typing import Any, Optional


def success(data: Any = None, message: str = "success", code: int = 200):
    """成功响应。

    Args:
        data: 响应数据
        message: 提示信息
        code: 状态码

    Returns:
        Flask 响应对象
    """
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code


def error(message: str = "error", code: int = 400, data: Any = None):
    """错误响应。

    Args:
        message: 错误信息
        code: 状态码
        data: 附加数据

    Returns:
        Flask 响应对象
    """
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code


def success_paginated(items: list, total: int, page: int, page_size: int, message: str = "success"):
    """分页成功响应。

    Args:
        items: 数据列表
        total: 总条数
        page: 当前页码
        page_size: 每页条数
        message: 提示信息

    Returns:
        Flask 响应对象
    """
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return jsonify({
        "code": 200,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    }), 200
