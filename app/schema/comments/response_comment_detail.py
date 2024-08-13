from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class CommentInformationForUser(BaseModel):
    id: int = Field(ge=1)
    content: str = Field(max_length=256)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    is_file_attached: bool = Field()


class CommentInformationForAdmin(BaseModel):
    id: int = Field(ge=1)
    content: str = Field(max_length=256)
    create_date: datetime = Field()
    update_date: Optional[datetime] = Field(None)
    is_file_attached: bool = Field()
    is_visible: bool = Field()


class ResponseCommentDetailForUser(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    detail: CommentInformationForUser
    file_name_list: List[str]

    @field_validator("role")
    def is_not_user(cls, value: str):
        if value != "ROLE_USER":
            raise ValueError("Role 불일치")
        return value


class ResponseCommentDetailForAdmin(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    detail: CommentInformationForAdmin
    file_name_list: List[str]

    @field_validator("role")
    def is_not_admin(cls, value: str):
        if value != "ROLE_ADMIN":
            raise ValueError("Role 불일치")
        return value
