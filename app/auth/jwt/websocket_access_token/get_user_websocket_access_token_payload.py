from typing import Annotated

from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError

from database.database import database_dependency
from auth.jwt.websocket_access_token.decode_websocket_access_token import (
    decode_websocket_access_token,
)
from auth.jwt.websocket_access_token.get_websocket_access_token_from_query import (
    websocket_access_token_dependency,
)
from data_wrapper.websocket_access_token_payload import WebsocketAccessTokenPayload
from config.config import get_settings
from exception_message import http_exception_params


def _validate_before_websocket_access_token():
    pass


def _validate_after_websocket_access_token(
    data_base: database_dependency, payload: dict
):
    try:
        sub: str = payload.get("sub")
        domain: str = payload.get(get_settings().APP_DOMAIN)
        user_id: int = payload.get("user_id")
        if (sub != "websocket_access_token") or (user_id is None) or (domain is None):
            raise InvalidTokenError()

    except InvalidTokenError:
        raise HTTPException(**http_exception_params.not_verified_token)

    return payload


def get_user_websocket_access_token_payload(
    data_base: database_dependency, token: websocket_access_token_dependency
) -> WebsocketAccessTokenPayload:
    _validate_before_websocket_access_token()
    payload = decode_websocket_access_token(encoded_access_token=token)
    _validate_after_websocket_access_token(data_base=data_base, payload=payload)

    return WebsocketAccessTokenPayload(payload)


def get_user_websocket_access_token_payload_without_query(
    data_base: database_dependency, token: str
) -> WebsocketAccessTokenPayload:
    _validate_before_websocket_access_token()
    payload = decode_websocket_access_token(encoded_websocket_access_token=token)
    _validate_after_websocket_access_token(data_base=data_base, payload=payload)

    return WebsocketAccessTokenPayload(payload)


current_user_websocket_access_token_payload = Annotated[
    WebsocketAccessTokenPayload, Depends(get_user_websocket_access_token_payload)
]
