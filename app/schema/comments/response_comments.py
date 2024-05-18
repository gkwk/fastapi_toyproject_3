from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

class CommentInformationForUser(BaseModel):
    id: int = Field(ge=1)
    user_id: int = Field(ge=1)
    content: str = Field(min_length=1, max_length=256)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    is_file_attached: bool = Field()


class CommentInformationForAdmin(BaseModel):
    id: int = Field(ge=1)
    user_id: int = Field(ge=1)
    content: str = Field(min_length=1, max_length=256)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    is_file_attached: bool = Field()
    is_visible: bool = Field()


class ResponseCommentsForUser(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    comments: List["CommentInformationForUser"]

    @field_validator("role")
    def is_not_user(cls, value: str):
        if value != "ROLE_USER":
            raise ValueError("Role 불일치")
        return value


class ResponseCommentsForAdmin(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    comments: List["CommentInformationForAdmin"]

    @field_validator("role")
    def is_not_admin(cls, value: str):
        if value != "ROLE_ADMIN":
            raise ValueError("Role 불일치")
        return value
