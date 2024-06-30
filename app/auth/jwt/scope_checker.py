from fastapi import HTTPException

from exception_message import http_exception_params
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def scope_checker(
    target_scopes: list, token: current_user_access_token_payload
):
    target_scopes_set = set(target_scopes)

    if not target_scopes_set.issubset(token.scope):
        raise HTTPException(**http_exception_params.not_verified_token)
