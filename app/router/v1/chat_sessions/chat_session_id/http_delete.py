from fastapi import HTTPException, Path

from database.database import database_dependency
from models import ChatSession
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message.http_exception_params import http_exception_params


def delete_chat_session(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int,
):
    chat_session = data_base.query(ChatSession).filter_by(id=chat_session_id).first()

    if token.get("user_id") != chat_session.user_create_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    data_base.delete(chat_session)
    data_base.commit()


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    chat_session_id: int = Path(ge=1),
):
    """
    채팅 세션을 삭제한다.
    """
    delete_chat_session(
        data_base=data_base, token=token, chat_session_id=chat_session_id
    )
