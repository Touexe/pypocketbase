from datetime import datetime

from .base import baseModel


class Admin(baseModel):
    id: str
    email: str
    avatar: int
    created: datetime
    updated: datetime
