from database.database import database_dependency
from models import ChatSession
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.request_chat_session_create import RequestChatSessionCreate


def logic_create_chat_session(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionCreate,
):
    chat_session = ChatSession(
        name=schema.name,
        user_create_id=token.user_id,
        information=schema.information,
        is_visible=schema.is_visible,
        is_closed=schema.is_closed,
    )

    return chat_session
