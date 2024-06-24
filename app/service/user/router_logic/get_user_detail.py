from fastapi import HTTPException

from database.database import database_dependency
from exception_message import http_exception_params
from service.user.logic_get_user_with_id import logic_get_user_with_id


def get_user_detail(data_base: database_dependency, user_id: int):
    user = logic_get_user_with_id(data_base=data_base, user_id=user_id)

    if user is None:
        raise HTTPException(**http_exception_params.not_exist_user)

    return user
