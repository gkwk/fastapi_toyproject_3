import secrets

from fastapi import HTTPException
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.users.user_id.router import router
from database.database import database_dependency
from models import User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from auth.jwt.password_context import get_password_context
from schema.users.request_user_detail_patch import RequestUserDetailPatch
from exception_message.http_exception_params import http_exception_params


def get_user_with_email(
    data_base: database_dependency,
    eamil: str,
):
    return data_base.query(User).filter_by(email=eamil).first()


def update_user_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestUserDetailPatch,
    user_id: int,
):   
    if token.get("user_id") != user_id:
        raise HTTPException(**http_exception_params["not_verified_token"])
    
    user = data_base.query(User).filter_by(id=token.get("user_id")).first()

    if not user:
        raise HTTPException(**http_exception_params["not_exist_user"])

    schema_dump = schema.model_dump()

    if (schema_dump.get("email") != None) and (
        get_user_with_email(data_base=data_base, eamil=schema.email)
    ):
        raise HTTPException(**http_exception_params["not_unique_email"])

    if schema_dump.get("email") != None:
        user.email = schema.email
    if (schema_dump.get("password1") != None) and (schema_dump.get("password1") != None):
        generated_password_salt = secrets.token_hex(4)
        user.password = get_password_context().hash(
            schema.password1 + generated_password_salt
        )
        user.password_salt = generated_password_salt

    data_base.add(user)
    data_base.commit()

    # 차후 access token 재발행 여부를 묻는 과정을 추가해도 될 것 같다.


@router.patch(v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT,tags=[v1_tags.USER_TAG])
def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestUserDetailPatch,
    user_id: int,
):
    """
    사용자 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    update_user_detail(data_base=data_base, token=token, schema=schema, user_id=user_id)