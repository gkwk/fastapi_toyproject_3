from fastapi import HTTPException

from database.database import database_dependency
from schema.users.request_user_join import RequestUserJoin
from service.user.logic_create_user import logic_create_user
from service.user.router_logic.create_user import create_user


def http_post(data_base: database_dependency, schema: RequestUserJoin):
    """
    사용자를 생성한다.
    """
    try:
        user = create_user(
            data_base=data_base,
            name=schema.name,
            password=schema.password1,
            email=schema.email,
        )
    except HTTPException as e:
        raise e

    return {"result": "success", "id": user.id}
