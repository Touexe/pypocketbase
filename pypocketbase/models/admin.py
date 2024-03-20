from datetime import datetime

from pydantic import BaseModel


class Admin(BaseModel):
    id: str
    email: str
    avatar: int
    created: datetime
    updated: datetime
