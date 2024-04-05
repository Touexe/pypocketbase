from .admin import Admin
from .base import baseModel
from .record import Record


class UserAuthResponse(baseModel):
    token: str
    record: Record


class AdminAuthResponse(baseModel):
    token: str
    admin: Admin
