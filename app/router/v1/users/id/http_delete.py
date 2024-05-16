from fastapi import HTTPException
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.users.id.router import router
from database.database import database_dependency
from models import User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from auth.jwt.refresh_token.delete_refresh_token import delete_refresh_token
from exception_message.http_exception_params import http_exception_params


def delete_user(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    user_id: int,
):
    if token.get("user_id") != user_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    user = data_base.query(User).filter_by(id=token.get("user_id")).first()

    data_base.delete(user)
    data_base.commit()

    # jwt list를 통해 refresh token과 access token을 삭제한다.
    delete_refresh_token(data_base=data_base, user_id=token.get("user_id"))


@router.delete(v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.USER_TAG])
def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    user_id: int,
):
    """
    사용자를 삭제한다.
    """
    delete_user(data_base=data_base, token=token, user_id=user_id)
