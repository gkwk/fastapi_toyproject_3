import secrets

from fastapi import HTTPException
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.router import router
from database.database import database_dependency
from models import ChatSession
from auth.jwt.password_context import get_password_context
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.request_chat_session_create import RequestChatSessionCreate
from exception_message.http_exception_params import http_exception_params


def create_chat_session(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionCreate,
):
    chat_session = ChatSession(
        name=schema.name,
        user_create_id=token.get("user_id"),
        information=schema.information,
        is_visible=schema.is_visible,
        is_closed=schema.is_closed,
    )
    data_base.add(chat_session)
    data_base.commit()

    return chat_session.id


@router.post(
    v1_url.ENDPOINT,
    status_code=status.HTTP_201_CREATED,
    tags=[v1_tags.CHAT_SESSION_TAG],
)
def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionCreate,
):
    """
    채팅 세션을 생성한다.
    """
    chatsession_id = create_chat_session(
        data_base=data_base, token=token, schema=schema
    )

    return {"result": "success", "id": chatsession_id}