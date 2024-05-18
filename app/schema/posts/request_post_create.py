from typing import List, Optional

from fastapi import Form, File, UploadFile, HTTPException
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from dataclasses import dataclass


class RequestPostCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1, max_length=1024)
    is_visible: bool = Field()

    @field_validator("name", "content")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value


@dataclass
class RequestFormPostCreate:
    name: str = Form(min_length=1, max_length=64)
    content: str = Form(min_length=1, max_length=1024)
    is_visible: bool = Form()
    files: List[Optional[UploadFile]] = File(None)

    @classmethod
    def from_form(
        cls,
        name: str = Form(min_length=1, max_length=64),
        content: str = Form(min_length=1, max_length=1024),
        is_visible: bool = Form(),
        files: List[Optional[UploadFile]] = File(None),
    ):
        try:
            RequestPostCreate(name=name, content=content, is_visible=is_visible)
            yield cls(name=name, content=content, is_visible=is_visible, files=files)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.json())
