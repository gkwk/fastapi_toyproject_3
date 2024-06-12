from fastapi import Path, HTTPException

from database.database import database_dependency
from models import Chat
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)

from exception_message.http_exception_params import http_exception_params


def get_chat_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int,
    chat_id: int,
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.

    chat = (
        data_base.query(Chat)
        .filter_by(id=chat_id, chat_session_id=chat_session_id)
        .first()
    )

    if not chat:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    return {
        "role": token.get("role"),
        "detail": chat,
    }


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
    chat_id: int = Path(ge=1),
):
    """
    채팅 세션의 챗 상세 정보를 조회한다.
    """
    return get_chat_detail(
        data_base=data_base,
        token=token,
        chat_session_id=chat_session_id,
        chat_id=chat_id,
    )
