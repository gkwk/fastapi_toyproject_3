from typing import Annotated

from fastapi import Depends

from database.database import database_dependency
from auth.jwt.refresh_token.validate_before_refresh_token import (
    validate_before_refresh_token,
)
from auth.jwt.refresh_token.validate_after_refresh_token import (
    validate_after_refresh_token,
)
from auth.jwt.refresh_token.decode_refresh_token import decode_refresh_token
from auth.jwt.refresh_token.get_refresh_token_from_cookie import (
    refresh_token_dependency,
)


def get_user_refresh_token_payload(
    data_base: database_dependency, token: refresh_token_dependency
):
    validate_before_refresh_token()
    payload = decode_refresh_token(encoded_refresh_token=token)
    validate_after_refresh_token(data_base=data_base, payload=payload)

    return payload


current_user_refresh_token_payload = Annotated[
    dict, Depends(get_user_refresh_token_payload)
]
