from fastapi import HTTPException

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


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    user_id: int,
):
    """
    사용자를 삭제한다.
    """
    delete_user(data_base=data_base, token=token, user_id=user_id)
