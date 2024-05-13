from typing import List

from pydantic import BaseModel, EmailStr, Field


class UserInformation(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(min_length=1, max_length=256)

class ResponseUsers(BaseModel):
    users: List["UserInformation"]