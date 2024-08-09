from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_admin_access_token_payload import (
    current_admin_access_token_payload,
)
from service.auth.router_logic.user_ban import user_ban
from schema.auth.request_user_ban import RequestUserBan


def http_post(
    data_base: database_dependency,
    token: current_admin_access_token_payload,
    schema: RequestUserBan,
):
    try:
        user_ban(data_base=data_base, user_id=schema.user_id, ban=schema.ban)
    except HTTPException as e:
        raise e

    return {"result": "success", "id": schema.user_id}
