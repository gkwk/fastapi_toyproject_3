from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.chat.router_logic.delete_chat import delete_chat


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
    chat_id: int = Path(ge=1),
):
    """
    채팅 세션의 챗을 삭제한다.
    """
    try:
        delete_chat(
            data_base=data_base,
            token=token,
            chat_session_id=chat_session_id,
            chat_id=chat_id,
        )
    except HTTPException as e:
        raise e
