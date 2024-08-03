from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.exc import OperationalError
from jwt.exceptions import InvalidTokenError

from database.database import database_dependency
from database.redis_method import blacklisted_access_token_cache_exist
from auth.jwt.access_token.decode_access_token import decode_access_token
from auth.jwt.oauth2_scheme import jwt_dependency
from data_wrapper.access_token_payload import AccessTokenPayload
from config.config import get_settings
from exception_message import http_exception_params


def _validate_before_decoding():
    pass


def _validate_after_decoding(
    data_base: database_dependency,
    payload: dict,
):
    try:
        sub: str = payload.get("sub")
        domain: str = payload.get(get_settings().APP_DOMAIN)
        user_name: str = payload.get("user_name")
        user_id: int = payload.get("user_id")
        token_uuid: str = payload.get("uuid")
        token_unix_timestamp: int = payload.get("exp")
        role : str = payload.get("role")

        if (
            (sub != "access_token")
            or (user_name is None)
            or (user_id is None)
            or (domain is None)
            or (token_uuid is None)
            or (token_unix_timestamp is None)
            or (role != "ROLE_ADMIN")
        ):
            raise InvalidTokenError()

        # access token 블랙리스트에서 동일한 uuid와 타임스탬프, user id값이 있는지 확인한다.
        if blacklisted_access_token_cache_exist(
            user_id=user_id, uuid=token_uuid, timestamp=token_unix_timestamp
        ):
            raise InvalidTokenError()

    except InvalidTokenError:
        raise HTTPException(**http_exception_params.not_verified_token)

    return payload


def get_admin_access_token_payload(
    data_base: database_dependency, token: jwt_dependency
) -> AccessTokenPayload:
    _validate_before_decoding()
    payload = decode_access_token(encoded_access_token=token)
    _validate_after_decoding(data_base=data_base, payload=payload)

    return AccessTokenPayload(payload)


def get_admin_access_token_payload_for_websocket(
    data_base: database_dependency, token: str
) -> AccessTokenPayload:
    _validate_before_decoding()
    payload = decode_access_token(encoded_access_token=token)
    _validate_after_decoding(data_base=data_base, payload=payload)

    return AccessTokenPayload(payload)


current_admin_access_token_payload = Annotated[
    AccessTokenPayload, Depends(get_admin_access_token_payload)
]
