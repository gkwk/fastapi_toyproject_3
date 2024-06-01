from typing import Annotated

from fastapi import Depends

from database.database import database_dependency
from auth.jwt.websocket_access_token.validate_before_websocket_access_token import (
    validate_before_websocket_access_token,
)
from auth.jwt.websocket_access_token.validate_after_websocket_access_token import (
    validate_after_websocket_access_token,
)
from auth.jwt.websocket_access_token.decode_websocket_access_token import decode_websocket_access_token
from auth.jwt.websocket_access_token.get_websocket_access_token_from_query import websocket_access_token_dependency


def get_user_websocket_access_token_payload(
    data_base: database_dependency, token: websocket_access_token_dependency
):
    validate_before_websocket_access_token()
    payload = decode_websocket_access_token(encoded_access_token=token)
    validate_after_websocket_access_token(data_base=data_base, payload=payload)

    return payload

def get_user_websocket_access_token_payload_without_query(
    data_base: database_dependency, token: str
):
    validate_before_websocket_access_token()
    payload = decode_websocket_access_token(encoded_websocket_access_token=token)
    validate_after_websocket_access_token(data_base=data_base, payload=payload)

    return payload

current_user_websocket_access_token_payload = Annotated[
    dict, Depends(get_user_websocket_access_token_payload)
]
