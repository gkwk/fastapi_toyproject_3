from fastapi import HTTPException
from jose import jwt, JWTError

from config.config import get_settings
from exception_message.http_exception_params import http_exception_params

SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM


def decode_websocket_access_token(encoded_websocket_access_token: str):
    credentials_exception = HTTPException(**http_exception_params["not_verified_token"])
    try:
        payload = jwt.decode(encoded_websocket_access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    return payload
