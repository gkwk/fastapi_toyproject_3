from typing import Annotated

from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from sqlalchemy.exc import OperationalError

from database.database import database_dependency
from auth.jwt.refresh_token.decode_refresh_token import decode_refresh_token
from auth.jwt.refresh_token.get_refresh_token_from_cookie import (
    refresh_token_dependency,
)
from data_wrapper.refresh_token_payload import RefreshTokenPayload
from config.config import get_settings
from exception_message import http_exception_params
from models import JWTList


def _get_jwt(
    data_base: database_dependency,
    user_id: int,
    refresh_token_uuid: str,
    refresh_token_unix_timestamp: int,
):
    try:
        # for update 쿼리 추가를 고려한다.
        jwt = (
            data_base.query(JWTList)
            .filter_by(
                user_id=user_id,
                refresh_token_uuid=refresh_token_uuid,
                refresh_token_unix_timestamp=refresh_token_unix_timestamp,
            )
            .limit(1)
            .first()
        )
    except OperationalError as e:
        raise HTTPException()

    return jwt


def _validate_before_decoding():
    pass


def _validate_after_decoding(data_base: database_dependency, payload: dict):
    try:
        sub: str = payload.get("sub")
        domain: str = payload.get(get_settings().APP_DOMAIN)
        user_id: int = payload.get("user_id")
        token_uuid: str = payload.get("uuid")
        token_unix_timestamp: int = payload.get("exp")

        if (
            (sub != "refresh_token")
            or (user_id is None)
            or (domain is None)
            or (token_uuid is None)
            or (token_unix_timestamp is None)
        ):
            raise InvalidTokenError()

        jwt = _get_jwt(
            data_base=data_base,
            user_id=user_id,
            refresh_token_uuid=token_uuid,
            refresh_token_unix_timestamp=token_unix_timestamp,
        )

        if jwt is None:
            raise InvalidTokenError()

    except InvalidTokenError:
        raise HTTPException(**http_exception_params.not_verified_token)

    return payload


def get_user_refresh_token_payload(
    data_base: database_dependency, token: refresh_token_dependency
) -> RefreshTokenPayload:
    _validate_before_decoding()
    payload = decode_refresh_token(encoded_refresh_token=token)
    _validate_after_decoding(data_base=data_base, payload=payload)

    return RefreshTokenPayload(payload)


current_user_refresh_token_payload = Annotated[
    RefreshTokenPayload, Depends(get_user_refresh_token_payload)
]
