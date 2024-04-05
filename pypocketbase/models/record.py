import datetime

from pydantic import BaseModel, ConfigDict, Field

from .base import baseModel


class Record(baseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    collection_id: str = Field(..., alias="collectionId")
    collection_name: str = Field(..., alias="collectionName")
    expand: dict | None = None
    created: datetime.datetime
    updated: datetime.datetime
