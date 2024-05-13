from typing import List, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator

class RequestBoardCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    information: str = Field(min_length=1, max_length=512)
    is_visible: Optional[bool] = Field(default=None)
    is_available: Optional[bool] = Field(default=None)
    user_id_list: Optional[List[int]] = Field(default=None)

    @field_validator("user_id_list")
    def id_validate(cls, value, info: ValidationInfo):
        for id in value:
            if id < 1:
                raise ValueError("id 에러")
        return value