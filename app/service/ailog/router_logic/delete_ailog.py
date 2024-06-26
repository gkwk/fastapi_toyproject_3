from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.ailog.logic_get_ailog import logic_get_ailog


def delete_ailog(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int,
    ailog_id: int,
):
    try:
        filter_dict = {"id": ailog_id, "ai_id": ai_id}
        if token.role != "ROLE_ADMIN":
            filter_dict["user_id"] = token.user_id

        ailog = logic_get_ailog(
            data_base=data_base,
            filter_dict=filter_dict,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )
    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if ailog is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    data_base.delete(ailog)

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
