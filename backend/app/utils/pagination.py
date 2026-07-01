"""分页工具。"""
from flask import request
from typing import Tuple, Any


def get_pagination_params() -> Tuple[int, int]:
    """获取分页参数。

    Returns:
        (page, page_size) 元组
    """
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 10

    return page, page_size


def paginate_query(query, page: int, page_size: int) -> dict:
    """对查询进行分页。

    Args:
        query: SQLAlchemy 查询对象
        page: 页码
        page_size: 每页条数

    Returns:
        包含 items, total, page, page_size, total_pages 的字典
    """
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
