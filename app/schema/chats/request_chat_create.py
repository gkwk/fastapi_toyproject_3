from typing import List, Optional

from fastapi import Form, File, UploadFile, HTTPException
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from dataclasses import dataclass


class RequestChatCreate(BaseModel):
    user_id: int = Field(ge=1)
    chat_session_id: int = Field(ge=1)
    content: str = Field(max_length=256)

    @field_validator("content")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value
