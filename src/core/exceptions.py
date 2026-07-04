from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.response import error_response


async def http_exception_handler(
    _request: Request,
    exc: HTTPException,
) -> JSONResponse:
    detail = exc.detail

    if isinstance(detail, dict):
        message = str(detail.get("message", "Request failed."))
        data = detail.get("data")
    else:
        message = str(detail)
        data = None

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=message,
            status_code=exc.status_code,
            data=data,
        ),
        headers=getattr(exc, "headers", None),
    )


async def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors: list[dict[str, Any]] = exc.errors()
    message = errors[0]["msg"] if errors else "Validation failed."

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=error_response(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            data={},
        ),
    )
