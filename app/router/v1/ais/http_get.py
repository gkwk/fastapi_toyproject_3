from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.ai.router_logic.get_ais import get_ais


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    AI 모델 목록을 조회한다.
    """
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.

    try:
        ais = get_ais(data_base=data_base)
    except HTTPException as e:
        raise e

    return {"role": token.role, "ais": ais}
