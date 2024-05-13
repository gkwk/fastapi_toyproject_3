from typing import List

from pydantic import BaseModel, Field, field_validator


class BoardInformationForUser(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    information: str = Field(max_length=512)


class BoardInformationForAdmin(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=64)
    information: str = Field(max_length=512)
    is_visible: bool = Field()
    is_available: bool = Field()
    permission_verified_user_id_range: int = Field(ge=0)


class ResponseBoardsForUser(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    boards: List["BoardInformationForUser"]
    
    @field_validator("role")
    def is_not_user(cls, value: str):
        if value != "ROLE_USER":
            raise ValueError("Role 불일치")
        return value


class ResponseBoardsForAdmin(BaseModel):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    role: str
    boards: List["BoardInformationForAdmin"]
    
    @field_validator("role")
    def is_not_admin(cls, value: str):
        if value != "ROLE_ADMIN":
            raise ValueError("Role 불일치")
        return value