import re
from typing import Optional, List

from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core.core_schema import ValidationInfo


class RequestBoardDetailPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    information: Optional[str] = Field(None, max_length=512)
    is_visible: Optional[bool] = Field(None)
    is_available: Optional[bool] = Field(None)
    user_list_permission_append: Optional[List[int]] = Field(None)
    user_list_permission_remove: Optional[List[int]] = Field(None)

    @field_validator("user_list_permission_append", "user_list_permission_remove")
    def id_validate(cls, value, info: ValidationInfo):
        for id in value:
            if id < 1:
                raise ValueError("id 에러")
        return value
