from typing import Self

from pydantic import BaseModel


class baseModel(BaseModel):
    @property
    def ok_value(self) -> Self:
        return self
