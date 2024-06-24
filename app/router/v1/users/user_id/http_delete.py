from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.user.router_logic.delete_user import delete_user


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    user_id: int,
):
    """
    사용자를 삭제한다.
    """
    try:
        delete_user(data_base=data_base, token=token, user_id=user_id)
    except HTTPException as e:
        raise e
