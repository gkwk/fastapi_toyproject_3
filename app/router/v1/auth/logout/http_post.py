from fastapi import Response

from database.database import database_dependency
from auth.jwt.refresh_token.delete_refresh_token import delete_refresh_token
from auth.jwt.access_token.ban_access_token import ban_access_token
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def http_post(
    response: Response,
    data_base: database_dependency,
    access_token: current_user_access_token_payload,
):
    user_id = access_token.get("user_id")
    response.delete_cookie(key="refresh_token")
    delete_refresh_token(data_base=data_base, user_id=user_id)

    return {"result": "success", "id": user_id}
