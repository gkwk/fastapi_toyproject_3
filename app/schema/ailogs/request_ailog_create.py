from typing import List, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class RequestAIlogCreate(BaseModel):
    ai_id: int = Field(ge=1)
    description: str = Field(min_length=1, max_length=256)

    @field_validator("description")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value
