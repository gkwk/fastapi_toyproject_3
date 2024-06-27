from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message.sql_exception_messages import integrity_exception_messages
from service.chat_session.logic_create_chat_session import logic_create_chat_session
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.request_chat_session_create import RequestChatSessionCreate


def create_chat_session(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionCreate,
):
    chat_session = logic_create_chat_session(
        data_base=data_base, token=token, schema=schema
    )

    data_base.add(chat_session)

    try:
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    return chat_session
