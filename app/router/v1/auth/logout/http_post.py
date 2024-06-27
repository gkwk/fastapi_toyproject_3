from fastapi import Response, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.auth.router_logic.logout import logout


def http_post(
    response: Response,
    data_base: database_dependency,
    access_token: current_user_access_token_payload,
):
    try:
        logout(response, data_base, access_token)

    except HTTPException as e:
        raise e

    return {"result": "success", "id": access_token.user_id}
