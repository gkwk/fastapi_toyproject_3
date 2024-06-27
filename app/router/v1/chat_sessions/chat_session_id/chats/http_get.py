from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.chat.router_logic.get_chats import get_chats


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
):
    """
    채팅 세션의 챗 목록을 조회한다.
    """
    try:
        chats = get_chats(
            data_base=data_base,
            chat_session_id=chat_session_id,
            user_id=token.user_id,
            user_role=token.role,
        )
    except HTTPException as e:
        raise e

    return {"role": token.role, "chats": chats}
