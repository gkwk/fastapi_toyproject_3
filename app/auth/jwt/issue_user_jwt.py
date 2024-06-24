from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import OperationalError

from models import User, JWTList, JWTAccessTokenBlackList
from database.database import database_dependency
from exception_message import http_exception_params
from auth.jwt.password_context import get_password_context
from auth.jwt.refresh_token.generate_refresh_token import generate_refresh_token
from auth.jwt.refresh_token.decode_refresh_token import decode_refresh_token
from auth.jwt.access_token.generate_access_token import generate_access_token
from auth.jwt.access_token.decode_access_token import decode_access_token
from auth.jwt.access_token.ban_access_token import ban_access_token


def _database_process(
    data_base: database_dependency,
    user: User,
    jwt: JWTList | None,
    access_token: str,
    refresh_token: str,
):
    refresh_token_payload = decode_refresh_token(refresh_token)
    uuid_refresh_token = refresh_token_payload.get("uuid")
    expired_date_refresh_token_unix_timestamp = refresh_token_payload.get("exp")

    access_token_payload = decode_access_token(access_token)
    access_token_uuid = access_token_payload.get("uuid")
    expired_date_access_token_unix_timestamp = access_token_payload.get("exp")

    if jwt:
        jwt.refresh_token_uuid = uuid_refresh_token
        jwt.refresh_token_unix_timestamp = expired_date_refresh_token_unix_timestamp
        jwt.access_token_uuid = access_token_uuid
        jwt.access_token_unix_timestamp = expired_date_access_token_unix_timestamp

        data_base.add(jwt)
    else:
        new_jwt = JWTList(
            user_id=user.id,
            refresh_token_uuid=uuid_refresh_token,
            refresh_token_unix_timestamp=expired_date_refresh_token_unix_timestamp,
            access_token_uuid=access_token_uuid,
            access_token_unix_timestamp=expired_date_access_token_unix_timestamp,
        )
        data_base.add(new_jwt)


def _validate_user(
    data_base: database_dependency,
    form_data: OAuth2PasswordRequestForm,
    user: User | None,
):
    if not user:
        raise HTTPException(**http_exception_params.not_exist_user)

    if user.is_banned:
        raise HTTPException(**http_exception_params.banned_user)

    if not get_password_context().verify(
        (form_data.password + user.password_salt), user.password
    ):
        raise HTTPException(**http_exception_params.not_verified_password)


def issue_user_jwt(
    data_base: database_dependency,
    form_data: OAuth2PasswordRequestForm,
):
    try:
        user = data_base.query(User).filter_by(name=form_data.username).limit(1).first()

        _validate_user(data_base=data_base, form_data=form_data, user=user)

        jwt = (
            data_base.query(JWTList)
            .filter_by(user_id=user.id)
            .limit(1)
            .with_for_update(nowait=True)
            .first()
        )

        if (
            (jwt is not None)
            and (jwt.access_token_uuid is not None)
            and (jwt.access_token_unix_timestamp is not None)
        ):
            blacklisted_access_token = (
                data_base.query(JWTAccessTokenBlackList)
                .filter_by(
                    user_id=user.id,
                    access_token_uuid=jwt.access_token_uuid,
                    access_token_unix_timestamp=jwt.access_token_unix_timestamp,
                )
                .limit(1)
                .with_for_update(nowait=True)
                .first()
            )
        else:
            blacklisted_access_token = None

        ban_access_token(
            data_base=data_base,
            jwt=jwt,
            blacklisted_access_token=blacklisted_access_token,
        )
        refresh_token = generate_refresh_token(user=user)
        access_token = generate_access_token(user=user)
        _database_process(
            data_base=data_base,
            user=user,
            jwt=jwt,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        data_base.commit()

    except OperationalError as e:
        raise HTTPException(status_code=400)

    # 발급된 refresh token은 로그인 페이지에서 쿠키로 전송하도록 조치한다.
    # return의 dict는 차후 dto로 변경한다.

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
