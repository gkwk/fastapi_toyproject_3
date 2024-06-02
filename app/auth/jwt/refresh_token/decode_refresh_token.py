from fastapi import HTTPException
import jwt
from jwt.exceptions import InvalidTokenError

from config.config import get_settings
from exception_message.http_exception_params import http_exception_params

SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM


def decode_refresh_token(encoded_refresh_token: str):
    credentials_exception = HTTPException(**http_exception_params["not_verified_token"])
    try:
        payload = jwt.decode(encoded_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception

    return payload
