from pydantic import BaseModel

from .admin import Admin
from .record import Record


class UserAuthResponse(BaseModel):
    token: str
    record: Record


class AdminAuthResponse(BaseModel):
    token: str
    admin: Admin
