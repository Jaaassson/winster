"""多语言工具。"""
import json
from flask import request
from typing import Any, Optional


def get_lang() -> str:
    """从请求头获取当前语言。

    Returns:
        语言代码，默认为 en-US
    """
    lang = request.headers.get("Accept-Language", "en-US")
    if lang.startswith("zh"):
        return "zh-CN"
    return "en-US"


def get_localized_value(value: Optional[any], lang: str = None) -> str:
    """从多语言字段获取对应语言的值。

    Args:
        value: JSON 格式的多语言字符串或字典
        lang: 语言代码，默认从请求头获取

    Returns:
        对应语言的值，如果找不到则返回英文或原值
    """
    if not value:
        return ""

    if lang is None:
        lang = get_lang()

    if isinstance(value, dict):
        return value.get(lang) or value.get("en-US") or value.get("zh-CN") or ""

    if isinstance(value, str):
        try:
            data = json.loads(value)
            if isinstance(data, dict):
                return data.get(lang) or data.get("en-US") or data.get("zh-CN") or ""
            return str(data)
        except (json.JSONDecodeError, TypeError):
            return value

    return str(value)


def get_i18n_field(json_str: Optional[str]) -> dict:
    """获取多语言字段的完整字典。

    Args:
        json_str: JSON 格式的多语言字符串

    Returns:
        多语言字典
    """
    if not json_str:
        return {"zh-CN": "", "en-US": ""}

    try:
        data = json.loads(json_str)
        if isinstance(data, dict):
            return {
                "zh-CN": data.get("zh-CN", ""),
                "en-US": data.get("en-US", "")
            }
        return {"zh-CN": str(data), "en-US": str(data)}
    except (json.JSONDecodeError, TypeError):
        return {"zh-CN": json_str, "en-US": json_str}
