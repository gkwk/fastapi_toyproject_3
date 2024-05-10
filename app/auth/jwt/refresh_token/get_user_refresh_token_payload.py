from typing import Annotated

from fastapi import Depends

from database.database import database_dependency
from auth.jwt.refresh_token.validate_before_refresh_token import (
    validate_before_refresh_token,
)
from app.auth.jwt.refresh_token.validate_after_refresh_token import (
    validate_after_refresh_token,
)
from auth.jwt.access_token.decode_access_token import decode_access_token
from auth.jwt.oauth2_scheme import jwt_dependency


def get_user_refresh_token_payload(
    data_base: database_dependency, token: jwt_dependency
):
    validate_after_refresh_token()
    payload = decode_access_token(encoded_access_token=token)
    validate_after_refresh_token()

    return payload


current_user_refresh_token_payload = Annotated[dict, Depends(get_user_refresh_token_payload)]
