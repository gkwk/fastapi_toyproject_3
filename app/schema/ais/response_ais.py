from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from enums import AIType


class AIInformationForUser(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    description: str = Field(max_length=256)
    ai_type: AIType = Field()


class AIInformationForAdmin(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    description: str = Field(max_length=256)
    ai_type: AIType = Field()
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    finish_date: Optional[datetime] = Field(None)
    is_visible: bool = Field()
    is_available: bool = Field()
    celery_task_id: Optional[str] = Field(None, max_length=64)


class ResponseAIsForUser(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str = Field()
    ais: List["AIInformationForUser"] = Field()

    @field_validator("role")
    def is_not_user(cls, value: str):
        if value != "ROLE_USER":
            raise ValueError("Role 불일치")
        return value


class ResponseAIsForAdmin(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str = Field()
    ais: List["AIInformationForAdmin"] = Field()

    @field_validator("role")
    def is_not_admin(cls, value: str):
        if value != "ROLE_ADMIN":
            raise ValueError("Role 불일치")
        return value
