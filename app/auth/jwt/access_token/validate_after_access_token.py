from fastapi import HTTPException
from jose import JWTError

from database.database import database_dependency
from config.config import get_settings
from execption_message.http_execption_params import http_exception_params


def validate_after_access_token(data_base: database_dependency, payload: dict):
    credentials_exception = HTTPException(**http_exception_params["not_verified_token"])

    try:
        domain: str = payload.get(get_settings().APP_DOMAIN)
        user_name: str = payload.get("user_name")
        user_id: int = payload.get("user_id")
        token = False  # access token 블랙리스트에서 동일한 uuid와 타임스탬프, user id값이 있는지 확인한다.

        if (user_name is None) or (user_id is None) or (token) or (domain is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return payload
