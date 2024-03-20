from pydantic import BaseModel


class ParamsList(BaseModel):
    page: int = 1
    size: int = 30
    filters: str = ""
    sort: str = "-created"
    expand: str = ""
    fields: str = ""


class ParamsOne(BaseModel):
    expand: str = ""
    fields: str = ""
