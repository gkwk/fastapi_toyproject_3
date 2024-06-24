from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.user.router_logic.get_user_detail import get_user_detail


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    user_id: int,
):
    """
    사용자 상세 정보를 조회한다.
    """
    try:
        user = get_user_detail(data_base=data_base, user_id=user_id)
    except HTTPException as e:
        raise e

    return user
