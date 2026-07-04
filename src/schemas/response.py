from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class PaginationMeta(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page: int = Field(ge=1)
    limit: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(alias="totalPages", ge=0)
    has_next_page: bool = Field(alias="hasNextPage")
    has_previous_page: bool = Field(alias="hasPreviousPage")


class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(populate_by_name=True)

    success: bool
    status_code: int = Field(alias="statusCode")
    message: str
    data: T | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(populate_by_name=True)

    success: bool
    status_code: int = Field(alias="statusCode")
    message: str
    meta: PaginationMeta
    data: list[T]
