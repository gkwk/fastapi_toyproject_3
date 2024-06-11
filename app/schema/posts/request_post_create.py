from typing import List, Optional

from fastapi import Form, File, UploadFile, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from dataclasses import dataclass


class RequestPostCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1, max_length=1024)
    is_visible: bool = Field()
    files: List[Optional[UploadFile]] = Field(None)

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
        request: Request,
        name: str = Form(min_length=1, max_length=64),
        content: str = Form(min_length=1, max_length=1024),
        is_visible: bool = Form(),
        files: List[Optional[UploadFile]] = File(None),
    ):
        # kwargs 사용이 어려우므로 locals() 를 사용해서 파라미터를 받아온다.
        local_parameters = locals()
        form_keys = request._form.keys()
        pydantic_model_parameters = {}

        for key in cls.__annotations__:
            if (key in form_keys) and (key in local_parameters):
                pydantic_model_parameters[key] = local_parameters[key]

        try:
            pydantic_model = RequestPostCreate(**pydantic_model_parameters)
            return pydantic_model
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=jsonable_encoder(e.errors()))
