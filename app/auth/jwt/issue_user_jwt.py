from fastapi.security import OAuth2PasswordRequestForm

from models import User, JWTList
from database.database import database_dependency
from auth.jwt.validate_before_issue_user_jwt import validate_before_issue_user_jwt
from auth.jwt.refresh_token.generate_refresh_token import generate_refresh_token
from auth.jwt.refresh_token.decode_refresh_token import decode_refresh_token
from auth.jwt.access_token.generate_access_token import generate_access_token
from auth.jwt.access_token.decode_access_token import decode_access_token
from auth.jwt.access_token.ban_access_token import ban_access_token


def database_process(
    data_base: database_dependency, user: User, access_token: str, refresh_token: str
):
    user_information = data_base.query(JWTList).filter_by(user_id=user.id).first()

    refresh_token_payload = decode_refresh_token(refresh_token)
    uuid_refresh_token = refresh_token_payload.get("uuid")
    expired_date_refresh_token_unix_timestamp = refresh_token_payload.get("exp")

    access_token_payload = decode_access_token(access_token)
    access_token_uuid = access_token_payload.get("uuid")
    expired_date_access_token_unix_timestamp = access_token_payload.get("exp")

    if user_information:
        user_information.refresh_token_uuid = uuid_refresh_token
        user_information.refresh_token_unix_timestamp = (
            expired_date_refresh_token_unix_timestamp
        )
        user_information.access_token_uuid = access_token_uuid
        user_information.access_token_unix_timestamp = (
            expired_date_access_token_unix_timestamp
        )
    else:
        user_information = JWTList(
            user_id=user.id,
            refresh_token_uuid=uuid_refresh_token,
            refresh_token_unix_timestamp=expired_date_refresh_token_unix_timestamp,
            access_token_uuid=access_token_uuid,
            access_token_unix_timestamp=expired_date_access_token_unix_timestamp,
        )

    data_base.add(user_information)
    data_base.commit()


def issue_user_jwt(
    data_base: database_dependency,
    form_data: OAuth2PasswordRequestForm,
):
    user = data_base.query(User).filter_by(name=form_data.username).first()

    validate_before_issue_user_jwt(data_base=data_base, form_data=form_data, user=user)
    ban_access_token(data_base=data_base, user_id=user.id)
    refresh_token = generate_refresh_token(data_base=data_base, user=user)
    access_token = generate_access_token(data_base=data_base, user=user)
    database_process(
        data_base=data_base,
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )

    # 발급된 refresh token은 로그인 페이지에서 쿠키로 전송하도록 조치한다.
    # return의 dict는 차후 dto로 변경한다.

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
