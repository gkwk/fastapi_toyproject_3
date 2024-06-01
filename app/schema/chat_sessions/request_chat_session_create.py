from typing import List, Optional

from fastapi import Form, File, UploadFile, HTTPException
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from dataclasses import dataclass


class RequestChatSessionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    information: str = Field(min_length=1, max_length=256)
    is_visible: bool = Field()
    is_closed: bool = Field()

    @field_validator("name", "information")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value
