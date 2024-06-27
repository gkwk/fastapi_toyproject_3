from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.chat_session.router_logic.get_chat_sessions import get_chat_sessions


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    채팅 세션 목록을 조회한다.
    """
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.

    try:
        chat_sessions = get_chat_sessions(
            data_base=data_base, filter_dict={"user_create_id": token.user_id}
        )
    except HTTPException as e:
        raise e

    return {"role": token.role, "chat_sessions": chat_sessions}
