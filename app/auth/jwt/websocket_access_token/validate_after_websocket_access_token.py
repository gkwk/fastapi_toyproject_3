from fastapi import HTTPException
from jose import JWTError

from database.database import database_dependency
from config.config import get_settings
from exception_message.http_exception_params import http_exception_params


def validate_after_websocket_access_token(
    data_base: database_dependency, payload: dict
):
    credentials_exception = HTTPException(**http_exception_params["not_verified_token"])

    try:
        sub: str = payload.get("sub")
        domain: str = payload.get(get_settings().APP_DOMAIN)
        user_id: int = payload.get("user_id")
        if (sub != "websocket_access_token") or (user_id is None) or (domain is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return payload
