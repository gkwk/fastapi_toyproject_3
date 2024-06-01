from fastapi import HTTPException, Path
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.chat_session_id.chats.chat_id.router import router
from database.database import database_dependency
from models import Chat
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message.http_exception_params import http_exception_params


def delete_chat(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int,
    chat_id: int,
):
    chat = data_base.query(Chat).filter_by(id=chat_id, chat_session_id=chat_session_id).first()

    if token.get("user_id") != chat.user_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    data_base.delete(chat)
    data_base.commit()


@router.delete(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.CHAT_TAG],
)
def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
    chat_id: int = Path(ge=1),
):
    """
    채팅 세션의 챗을 삭제한다.
    """
    delete_chat(data_base=data_base, token=token, chat_session_id=chat_session_id, chat_id=chat_id)
