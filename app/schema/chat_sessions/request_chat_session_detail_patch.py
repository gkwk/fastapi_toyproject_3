from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from pydantic_core import PydanticUndefinedType
from dataclasses import dataclass


class RequestChatSessionDetailPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=64)
    information: Optional[str] = Field(None, max_length=256)
    is_visible: Optional[bool] = Field(None)
    is_closed: Optional[bool] = Field(None)

    @field_validator("name", "information")
    def is_not_empty(cls, value: str):
        if (value == None) or (not value.strip()):
            raise ValueError("값이 공백일 수 없습니다.")
        return value
