from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.password_reset_token.get_user_password_reset_token_payload import (
    current_user_password_reset_token_payload,
)
from service.auth.router_logic.password_reset import password_reset
from schema.password_reset.request_user_password_reset import (
    RequestUserPasswordReset,
)


def http_patch(
    data_base: database_dependency,
    token: current_user_password_reset_token_payload,
    schema: RequestUserPasswordReset,
):
    try:
        password_reset(data_base=data_base, token=token, schema=schema)
    except HTTPException as e:
        raise e
