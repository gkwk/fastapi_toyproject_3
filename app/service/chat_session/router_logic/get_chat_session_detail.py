from fastapi import HTTPException

from database.database import database_dependency
from exception_message import http_exception_params
from service.chat_session.logic_get_chat_session import logic_get_chat_session
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def get_chat_session_detail(
    data_base: database_dependency,
    chat_session_id: int,
    token: current_user_access_token_payload,
):
    filter_dict = {"id": chat_session_id}
    if token.role != "ROLE_ADMIN":
        filter_dict["user_create_id"] = token.user_id

    chat_session = logic_get_chat_session(
        data_base=data_base,
        filter_dict=filter_dict,
    )

    if chat_session is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    return chat_session
