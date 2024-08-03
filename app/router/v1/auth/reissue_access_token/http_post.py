from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.reissue_access_token import reissue_access_token
from auth.jwt.refresh_token.get_user_refresh_token_payload import (
    current_user_refresh_token_payload,
)


def http_post(data_base: database_dependency, token: current_user_refresh_token_payload):
    try:
        tokens = reissue_access_token(data_base=data_base, refresh_token_payload=token)

    except HTTPException as e:
        raise e

    return {
        "access_token": tokens.get("access_token"),
        "token_type": tokens.get("token_type"),
    }
