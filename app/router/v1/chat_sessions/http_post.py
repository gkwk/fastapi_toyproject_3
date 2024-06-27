from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.request_chat_session_create import RequestChatSessionCreate
from service.chat_session.router_logic.create_chat_session import (
    create_chat_session,
)


def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionCreate,
):
    """
    채팅 세션을 생성한다.
    """

    try:
        chatsession = create_chat_session(
            data_base=data_base, token=token, schema=schema
        )

    except HTTPException as e:
        raise e

    return {"result": "success", "id": chatsession.id}
