from typing import List, Optional

from fastapi import Form, File, UploadFile, HTTPException
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from dataclasses import dataclass


class RequestCommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1024)
    is_visible: bool = Field()

    @field_validator("content")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value


@dataclass
class RequestFormCommentCreate:
    content: str = Form(min_length=1, max_length=256)
    is_visible: bool = Form()
    files: List[Optional[UploadFile]] = File(None)

    # 불필요한 key값들이 전달되면 422를 반환하도록 수정이 필요하다.
    @classmethod
    def from_form(
        cls,
        content: str = Form(min_length=1, max_length=256),
        is_visible: bool = Form(),
        files: List[Optional[UploadFile]] = File(None),
    ):
        try:
            RequestCommentCreate(content=content, is_visible=is_visible)
            yield cls(content=content, is_visible=is_visible, files=files)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.json())
