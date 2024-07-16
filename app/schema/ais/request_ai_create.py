from typing import List, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from enums import AIType

class RequestAICreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1, max_length=256)
    is_visible: bool = Field(default=True)
    ai_type : AIType = Field()

    @field_validator("name", "description")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value
