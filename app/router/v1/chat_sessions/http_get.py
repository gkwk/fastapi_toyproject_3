from typing import Union

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.router import router
from database.database import database_dependency
from models import ChatSession
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.response_chat_sessions import (
    ResponseChatSessionsForUser,
    ResponseChatSessionsForAdmin,
)


def get_chat_sessions(
    data_base: database_dependency, token: current_user_access_token_payload
):
    return {
        "role": token.get("role"),
        "chat_sessions": data_base.query(ChatSession).filter_by().all(),
    }


@router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseChatSessionsForUser, ResponseChatSessionsForAdmin],
    tags=[v1_tags.CHAT_SESSION_TAG],
)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    채팅 세션 목록을 조회한다.
    """
    return get_chat_sessions(data_base=data_base, token=token)
