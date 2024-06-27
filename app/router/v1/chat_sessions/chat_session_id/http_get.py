from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.chat_session.router_logic.get_chat_session_detail import (
    get_chat_session_detail,
)


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
):
    """
    채팅 세션 정보를 조회한다.
    """
    try:
        chat_session = get_chat_session_detail(
            data_base=data_base, chat_session_id=chat_session_id, token=token
        )
    except HTTPException as e:
        raise e

    return {"role": token.role, "detail": chat_session}
