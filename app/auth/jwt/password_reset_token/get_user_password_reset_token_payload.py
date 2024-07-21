from typing import Annotated

from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError

from database.database import database_dependency
from auth.jwt.password_reset_token.decode_password_reset_token import (
    decode_password_reset_token,
)
from auth.jwt.password_reset_token.get_password_reset_token_from_path import (
    password_reset_token_dependency,
)
from data_wrapper.password_reset_token_payload import PasswordResetTokenPayload
from config.config import get_settings
from exception_message import http_exception_params


def _validate_before_password_reset_token():
    pass


def _validate_after_password_reset_token(
    data_base: database_dependency, payload: dict
):
    try:
        sub: str = payload.get("sub")
        domain: str = payload.get(get_settings().APP_DOMAIN)
        user_id: int = payload.get("user_id")
        if (sub != "password_reset_token") or (user_id is None) or (domain is None):
            raise InvalidTokenError()

    except InvalidTokenError:
        raise HTTPException(**http_exception_params.not_verified_token)

    return payload


def get_user_password_reset_token_payload(
    data_base: database_dependency, token: password_reset_token_dependency
) -> PasswordResetTokenPayload:
    _validate_before_password_reset_token()
    payload = decode_password_reset_token(encoded_password_reset_token=token)
    _validate_after_password_reset_token(data_base=data_base, payload=payload)

    return PasswordResetTokenPayload(payload)


def get_user_password_reset_token_payload_without_path(
    data_base: database_dependency, token: str
) -> PasswordResetTokenPayload:
    _validate_before_password_reset_token()
    payload = decode_password_reset_token(encoded_password_reset_token=token)
    _validate_after_password_reset_token(data_base=data_base, payload=payload)

    return PasswordResetTokenPayload(payload)


current_user_password_reset_token_payload = Annotated[
    PasswordResetTokenPayload, Depends(get_user_password_reset_token_payload)
]
