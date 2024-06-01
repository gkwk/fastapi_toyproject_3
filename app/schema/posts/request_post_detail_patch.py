import uuid
from typing import Optional, List, TypedDict, Annotated

from fastapi import Form, File, UploadFile, HTTPException, Request, Depends
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ValidationError
from pydantic_core import PydanticUndefinedType
from dataclasses import dataclass


class RequestPostDetailPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    content: Optional[str] = Field(None, min_length=1, max_length=1024)
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

    @field_validator("name", "content")
    def is_not_empty(cls, value: str):
        if (value == None) or (not value.strip()):
            raise ValueError("값이 공백일 수 없습니다.")
        return value


def get_refresh_token_from_cookie(request: Request):
    refresh_token = request.cookies.get("refresh_token", "")

    return refresh_token


@dataclass
class RequestFormPostDetailPatch:
    name: Optional[str] = Form(None, min_length=1, max_length=64)
    content: Optional[str] = Form(None, min_length=1, max_length=1024)
    is_visible: Optional[bool] = Form(None)
    file_list_append: List[Optional[UploadFile]] = File(None)
    file_list_remove: List[Optional[str]] = Form(None)

    @classmethod
    def to_pydantic(
        cls,
        request: Request,
        name: Optional[str] = Form(None, min_length=1, max_length=64),
        content: Optional[str] = Form(None, min_length=1, max_length=1024),
        is_visible: Optional[bool] = Form(None),
        file_list_append: List[Optional[UploadFile]] = File(None),
        file_list_remove: List[Optional[str]] = Form(None),
    ):
        # kwargs 사용이 어려우므로 locals() 를 사용해서 파라미터를 받아온다.
        local_parameters = locals()
        form_keys =  request._form.keys()
        pydantic_model_parameters = {}

        for key in cls.__annotations__:
            if (key in local_parameters) and (key in form_keys):
                pydantic_model_parameters[key] = local_parameters[key]

        try:
            pydantic_model = RequestPostDetailPatch(**pydantic_model_parameters)
            yield pydantic_model
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.json())


# @dataclass
# class RequestFormPostDetailPatch:
#     name: Optional[str] = Form(PydanticUndefinedType, min_length=1, max_length=64)
#     content: Optional[str] = Form(PydanticUndefinedType, min_length=1, max_length=1024)
#     is_visible: Optional[bool] = Form(PydanticUndefinedType)
#     file_list_append: List[Optional[UploadFile]] = File(PydanticUndefinedType)
#     file_list_remove: List[Optional[str]] = Form(PydanticUndefinedType)

#     @classmethod
#     def to_pydantic(
#         cls,
#         name: Optional[str] = Form(PydanticUndefinedType, min_length=1, max_length=64),
#         content: Optional[str] = Form(
#             PydanticUndefinedType, min_length=1, max_length=1024
#         ),
#         is_visible: Optional[bool] = Form(PydanticUndefinedType),
#         file_list_append: List[Optional[UploadFile]] = File(PydanticUndefinedType),
#         file_list_remove: List[Optional[str]] = Form(PydanticUndefinedType),
#     ):
#         # kwargs 사용이 어려우므로 locals() 를 사용해서 파라미터를 받아온다.
#         local_parameters = locals()
#         pydantic_model_parameters = {}

#         for key in cls.__annotations__:
#             if (key in local_parameters) and (
#                 local_parameters.get(key, PydanticUndefinedType)
#                 is not PydanticUndefinedType
#             ):
#                 pydantic_model_parameters[key] = local_parameters[key]

#         try:
#             pydantic_model = RequestPostDetailPatch(**pydantic_model_parameters)
#             yield pydantic_model
#         except ValidationError as e:
#             raise HTTPException(status_code=422, detail=e.json())
