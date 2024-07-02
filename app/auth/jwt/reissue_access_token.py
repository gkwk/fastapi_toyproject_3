from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from models import User, JWTList
from database.database import database_dependency
from exception_message import http_exception_params
from auth.jwt.refresh_token.get_user_refresh_token_payload import (
    current_user_refresh_token_payload,
)
from auth.jwt.access_token.generate_access_token import generate_access_token
from auth.jwt.access_token.decode_access_token import decode_access_token
from auth.jwt.access_token.ban_access_token import ban_access_token


def _database_process(
    data_base: database_dependency, user: User, jwt: JWTList | None, access_token: str
):
    access_token_payload = decode_access_token(access_token)
    access_token_uuid = access_token_payload.get("uuid")
    expired_date_access_token_unix_timestamp = access_token_payload.get("exp")

    if jwt:
        jwt.access_token_uuid = access_token_uuid
        jwt.access_token_unix_timestamp = expired_date_access_token_unix_timestamp
        data_base.add(jwt)


def _validate_user(data_base: database_dependency, user: User | None):
    if not user:
        raise HTTPException(**http_exception_params.not_exist_user)

    if user.is_banned:
        raise HTTPException(**http_exception_params.banned_user)


def reissue_access_token(
    data_base: database_dependency,
    refresh_token_payload: current_user_refresh_token_payload,
):
    try:
        user = (
            data_base.query(User)
            .filter_by(id=refresh_token_payload.get("user_id"))
            .limit(1)
            .first()
        )

        _validate_user(data_base=data_base, user=user)

        jwt = (
            data_base.query(JWTList)
            .filter_by(user_id=user.id)
            .limit(1)
            .with_for_update(nowait=True)
            .first()
        )

        ban_access_token(
            data_base=data_base,
            jwt=jwt,
        )

        access_token = generate_access_token(user=user)
        _database_process(
            data_base=data_base, user=user, jwt=jwt, access_token=access_token
        )

        data_base.commit()

    except OperationalError as e:
        raise HTTPException(status_code=400)

    # return의 dict는 차후 dto로 변경한다.

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
