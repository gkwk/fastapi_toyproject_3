from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class PostInformationForUser(BaseModel):
    id: int = Field(ge=1)
    user_id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1, max_length=1024)
    board_id: int = Field(ge=1)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    number_of_view: int = Field(ge=0)
    number_of_comment: int = Field(ge=0)
    number_of_like: int = Field(ge=0)
    is_file_attached: bool = Field()


class PostInformationForAdmin(BaseModel):
    id: int = Field(ge=1)
    user_id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1, max_length=1024)
    board_id: int = Field(ge=1)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    number_of_view: int = Field(ge=0)
    number_of_comment: int = Field(ge=0)
    number_of_like: int = Field(ge=0)
    is_file_attached: bool = Field()
    is_visible: bool = Field()


class ResponsePostsForUser(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    posts: List["PostInformationForUser"]

    @field_validator("role")
    def is_not_user(cls, value: str):
        if value != "ROLE_USER":
            raise ValueError("Role 불일치")
        return value


class ResponsePostsForAdmin(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    posts: List["PostInformationForAdmin"]

    @field_validator("role")
    def is_not_admin(cls, value: str):
        if value != "ROLE_ADMIN":
            raise ValueError("Role 불일치")
        return value
