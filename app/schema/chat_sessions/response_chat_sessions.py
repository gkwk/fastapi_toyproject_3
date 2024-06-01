from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ChatSessionInformationForUser(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    information: str = Field(min_length=1, max_length=256)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    is_closed: bool = Field()


class ChatSessionInformationForAdmin(BaseModel):
    id: int = Field(ge=1)
    user_create_id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    information: str = Field(min_length=1, max_length=256)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    is_visible: bool = Field()
    is_closed: bool = Field()


class ResponseChatSessionsForUser(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    chat_sessions: List["ChatSessionInformationForUser"]

    @field_validator("role")
    def is_not_user(cls, value: str):
        if value != "ROLE_USER":
            raise ValueError("Role 불일치")
        return value


class ResponseChatSessionsForAdmin(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    chat_sessions: List["ChatSessionInformationForAdmin"]

    @field_validator("role")
    def is_not_admin(cls, value: str):
        if value != "ROLE_ADMIN":
            raise ValueError("Role 불일치")
        return value
