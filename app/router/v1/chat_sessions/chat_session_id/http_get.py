from typing import Union

from fastapi import Path, HTTPException

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.chat_session_id.router import router
from database.database import database_dependency
from models import ChatSession
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.response_chat_session_detail import (
    ResponseChatSessionDetailForUser,
    ResponseChatSessionDetailForAdmin,
)
from exception_message.http_exception_params import http_exception_params


def get_chat_session_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int,
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.

    chat_session = data_base.query(ChatSession).filter_by(id=chat_session_id).first()

    if not chat_session:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    return {
        "role": token.get("role"),
        "detail": chat_session,
    }


@router.get(
    v1_url.ENDPOINT,
    response_model=Union[
        ResponseChatSessionDetailForUser, ResponseChatSessionDetailForAdmin
    ],
    tags=[v1_tags.CHAT_SESSION_TAG],
)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
):
    """
    채팅 세션 정보를 조회한다.
    """
    return get_chat_session_detail(
        data_base=data_base, token=token, chat_session_id=chat_session_id
    )
