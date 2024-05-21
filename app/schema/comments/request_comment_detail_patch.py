import uuid
from datetime import datetime
from typing import Optional, List, TypedDict, Annotated

from fastapi import Form, File, UploadFile, HTTPException
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from pydantic_core import PydanticUndefinedType
from dataclasses import dataclass


class RequestCommentDetailPatch(BaseModel):
    content: Optional[str] = Field(None, max_length=256)
    is_visible: Optional[bool] = Field(None)
    file_list_append: List[Optional[UploadFile]] = File(None)
    file_list_remove: List[Optional[str]] = Field(None)

    @field_validator("file_list_remove")
    def uuid_validate(cls, value, info: ValidationInfo):
        for uuid_str in value:
            try:
                uuid.UUID(hex=uuid_str)
            except Exception:
                raise ValueError("uuid 에러")
        return value

    @field_validator("content")
    def is_not_empty(cls, value: str):
        if (value == None) or (not value.strip()):
            raise ValueError("값이 공백일 수 없습니다.")
        return value


@dataclass
class RequestFormCommentDetailPatch:
    content: Optional[str] = Form(PydanticUndefinedType, max_length=256)
    is_visible: Optional[bool] = Form(PydanticUndefinedType)
    file_list_append: List[Optional[UploadFile]] = File(PydanticUndefinedType)
    file_list_remove: List[Optional[str]] = Form(PydanticUndefinedType)

    @classmethod
    def to_pydantic(
        cls,
        content: Optional[str] = Form(PydanticUndefinedType, max_length=256),
        is_visible: Optional[bool] = Form(PydanticUndefinedType),
        file_list_append: List[Optional[UploadFile]] = File(PydanticUndefinedType),
        file_list_remove: List[Optional[str]] = Form(PydanticUndefinedType),
    ):
        # kwargs 사용이 어려우므로 locals() 를 사용해서 파라미터를 받아온다.
        local_parameters = locals()
        pydantic_model_parameters = {}

        for key in cls.__annotations__:
            if (key in local_parameters) and (
                local_parameters.get(key, PydanticUndefinedType)
                is not PydanticUndefinedType
            ):
                pydantic_model_parameters[key] = local_parameters[key]

        try:
            pydantic_model = RequestCommentDetailPatch(**pydantic_model_parameters)
            yield pydantic_model
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.json())
