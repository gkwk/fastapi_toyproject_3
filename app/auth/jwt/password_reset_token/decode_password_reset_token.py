from fastapi import HTTPException
import jwt
from jwt.exceptions import InvalidTokenError

from config.config import get_settings
from exception_message import http_exception_params

SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM


def decode_password_reset_token(encoded_password_reset_token: str):
    try:
        payload = jwt.decode(
            encoded_password_reset_token, SECRET_KEY, algorithms=[ALGORITHM]
        )
    except InvalidTokenError:
        raise HTTPException(**http_exception_params.not_verified_token)

    return payload
