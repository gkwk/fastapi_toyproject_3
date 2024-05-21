from fastapi import HTTPException
from jose import JWTError

from database.database import database_dependency
from config.config import get_settings
from exception_message.http_exception_params import http_exception_params
from models import JWTList


def validate_after_refresh_token(data_base: database_dependency, payload: dict):
    credentials_exception = HTTPException(**http_exception_params["not_verified_token"])

    try:
        sub: str = payload.get("sub")
        domain: str = payload.get(get_settings().APP_DOMAIN)
        user_id: int = payload.get("user_id")
        user_validation_information = (
            data_base.query(JWTList).filter_by(user_id=user_id).first()
        )
        token_uuid: str = payload.get("uuid")
        token_unix_timestamp: int = payload.get("exp")

        if (
            (sub != "refresh_token")
            or (user_id is None)
            or (user_validation_information is None)
            or (domain is None)
            or not (
                (token_uuid == user_validation_information.refresh_token_uuid)
                and (
                    token_unix_timestamp
                    == user_validation_information.refresh_token_unix_timestamp
                )
            )
        ):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return payload
