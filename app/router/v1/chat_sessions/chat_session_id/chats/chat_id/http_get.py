from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.chat.router_logic.get_chat_detail import get_chat_detail


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
    chat_id: int = Path(ge=1),
):
    """
    채팅 세션의 챗 상세 정보를 조회한다.
    """

    try:
        chat = get_chat_detail(
            data_base=data_base,
            chat_session_id=chat_session_id,
            chat_id=chat_id,
            token=token,
        )
    except HTTPException as e:
        raise e

    return {"role": token.role, "detail": chat}
