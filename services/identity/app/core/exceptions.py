"""
Global exception handler
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from .responses import standard_error_response


class IdentityException(Exception):
    status_code = 400
    message = "Something went wrong"

    def __init__(self, message: str | None = None, errors: dict | None = None):
        self.message = message or self.message
        self.errors = errors or {}
        super().__init__(self.message)  # calling base Exception class constructor


async def identity_exception_handler(
    request: Request, exc: IdentityException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=standard_error_response(message=exc.message, errors=exc.errors),
    )
