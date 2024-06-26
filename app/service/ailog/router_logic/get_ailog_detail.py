from fastapi import HTTPException

from database.database import database_dependency
from exception_message import http_exception_params
from service.ailog.logic_get_ailog import logic_get_ailog


def get_ailog_detail(
    data_base: database_dependency,
    ai_id: int,
    ailog_id: int,
    user_id: int,
    user_role: str,
):
    filter_dict = {"id": ailog_id, "ai_id": ai_id}

    if user_role != "ROLE_ADMIN":
        filter_dict["user_id"] = user_id

    ailog = logic_get_ailog(data_base=data_base, filter_dict=filter_dict)

    if ailog is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    return ailog
