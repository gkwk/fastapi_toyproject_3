from fastapi import HTTPException

from database.database import database_dependency
from exception_message import http_exception_params
from service.ai.logic_get_ai_with_id import logic_get_ai_with_id


def get_ai_detail(data_base: database_dependency, ai_id: int):
    ai = logic_get_ai_with_id(data_base=data_base, ai_id=ai_id)

    if ai is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    return ai
