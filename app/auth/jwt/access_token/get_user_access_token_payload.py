from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.exc import OperationalError
from jwt.exceptions import InvalidTokenError

from database.database import database_dependency
from auth.jwt.access_token.decode_access_token import decode_access_token
from auth.jwt.oauth2_scheme import jwt_dependency
from data_wrapper.access_token_payload import AccessTokenPayload
from config.config import get_settings
from exception_message import http_exception_params
from models import JWTAccessTokenBlackList


def _get_blacklisted_access_token(
    data_base: database_dependency,
    user_id: int,
    access_token_uuid: str,
    access_token_unix_timestamp: int,
):
    try:
        # for update 쿼리 추가를 고려한다.
        blacklisted_access_token = (
            data_base.query(JWTAccessTokenBlackList)
            .filter_by(
                user_id=user_id,
                access_token_uuid=access_token_uuid,
                access_token_unix_timestamp=access_token_unix_timestamp,
            )
            .limit(1)
            .first()
        )
    except OperationalError as e:
        raise HTTPException(status_code=400)

    return blacklisted_access_token


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

        if (
            (sub != "access_token")
            or (user_name is None)
            or (user_id is None)
            or (domain is None)
            or (token_uuid is None)
            or (token_unix_timestamp is None)
        ):
            raise InvalidTokenError()

        blacklisted_access_token = _get_blacklisted_access_token(
            data_base=data_base,
            user_id=user_id,
            access_token_uuid=token_uuid,
            access_token_unix_timestamp=token_unix_timestamp,
        )

        # access token 블랙리스트에서 동일한 uuid와 타임스탬프, user id값이 있는지 확인한다.
        if blacklisted_access_token is not None:
            raise InvalidTokenError()

    except InvalidTokenError:
        raise HTTPException(**http_exception_params.not_verified_token)

    return payload


def get_user_access_token_payload(
    data_base: database_dependency, token: jwt_dependency
) -> AccessTokenPayload:
    _validate_before_decoding()
    payload = decode_access_token(encoded_access_token=token)
    _validate_after_decoding(data_base=data_base, payload=payload)

    return AccessTokenPayload(payload)


def get_user_access_token_payload_for_websocket(
    data_base: database_dependency, token: str
) -> AccessTokenPayload:
    _validate_before_decoding()
    payload = decode_access_token(encoded_access_token=token)
    _validate_after_decoding(data_base=data_base, payload=payload)

    return AccessTokenPayload(payload)


current_user_access_token_payload = Annotated[
    AccessTokenPayload, Depends(get_user_access_token_payload)
]
