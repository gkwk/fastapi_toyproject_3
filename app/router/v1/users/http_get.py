from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.user.router_logic.get_users import get_users


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    사용자 목록을 조회한다.
    """
    try:
        users = get_users(data_base=data_base)
    except HTTPException as e:
        raise e

    return {"users": users}
