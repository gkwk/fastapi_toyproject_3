from typing import Union

from fastapi import Path
from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.chat_session_id.chats.router import router
from database.database import database_dependency
from models import Chat
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chats.response_chats import (
    ResponseChatsForUser,
    ResponseChatsForAdmin,
)


def get_chats(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int,
):
    return {
        "role": token.get("role"),
        "chats": data_base.query(Chat).filter_by(chat_session_id=chat_session_id).all(),
    }


@router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseChatsForUser, ResponseChatsForAdmin],
    tags=[v1_tags.CHAT_TAG],
)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
):
    """
    채팅 세션의 챗 목록을 조회한다.
    """
    return get_chats(data_base=data_base, token=token, chat_session_id=chat_session_id)
