from pydantic import BaseModel, Field

from .base import baseModel
from .record import Record


class ListResult(baseModel):
    page: int = Field(..., alias="page")
    per_page: int = Field(..., alias="perPage")
    total_items: int = Field(..., alias="totalItems")
    total_pages: int = Field(..., alias="totalPages")
    items: list[Record] = []
