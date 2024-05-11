from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ResponseUserDetail(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(min_length=1, max_length=256)
    join_date: datetime
