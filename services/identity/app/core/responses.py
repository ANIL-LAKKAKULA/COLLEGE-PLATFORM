"""
Standard sucess and error responses
"""

from typing import Any


def standard_success_response(message: str = "Success", data: Any = None) -> dict:
    return {"success": True, "message": message, "data": data or {}}


def standard_error_response(message: str, errors: dict | None = None) -> dict:
    return {"success": False, "message": message, "errors": errors or {}}
