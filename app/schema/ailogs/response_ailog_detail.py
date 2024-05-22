from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class AIlogInformationForUser(BaseModel):
    id: int = Field(ge=1)
    description: str = Field(max_length=256)
    result: str = Field(max_length=256)
    create_date: datetime = Field()
    is_finished: bool = Field()


class AIlogInformationForAdmin(BaseModel):
    id: int = Field(ge=1)
    user_id: int = Field(ge=1)
    description: str = Field(max_length=256)
    result: str = Field(max_length=256)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    finish_date: Optional[datetime] = Field(None)
    is_finished: bool = Field()
    celery_task_id: str = Field(max_length=64)


class ResponseAIlogDetailForUser(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    detail: AIlogInformationForUser

    @field_validator("role")
    def is_not_user(cls, value: str):
        if value != "ROLE_USER":
            raise ValueError("Role 불일치")
        return value


class ResponseAIlogDetailForAdmin(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    detail: AIlogInformationForAdmin

    @field_validator("role")
    def is_not_admin(cls, value: str):
        if value != "ROLE_ADMIN":
            raise ValueError("Role 불일치")
        return value
