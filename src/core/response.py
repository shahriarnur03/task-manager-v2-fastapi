from math import ceil
from typing import Any


def success_response(
    message: str,
    data: Any = None,
    status_code: int = 200,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "success": True,
        "statusCode": status_code,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return response


def paginated_response(
    message: str,
    data: Any,
    page: int,
    limit: int,
    total: int,
    status_code: int = 200,
) -> dict[str, Any]:
    total_pages = ceil(total / limit) if total else 0

    return {
        "success": True,
        "statusCode": status_code,
        "message": message,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": total_pages,
            "hasNextPage": page < total_pages,
            "hasPreviousPage": page > 1,
        },
        "data": data,
    }


def error_response(
    message: str,
    status_code: int,
    data: Any = None,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "success": False,
        "statusCode": status_code,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return response
