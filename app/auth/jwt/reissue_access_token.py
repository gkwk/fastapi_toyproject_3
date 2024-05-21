from fastapi.security import OAuth2PasswordRequestForm

from models import User, JWTList
from database.database import database_dependency
from auth.jwt.validate_before_issue_user_jwt import validate_before_issue_user_jwt
from auth.jwt.refresh_token.get_user_refresh_token_payload import current_user_refresh_token_payload
from auth.jwt.access_token.generate_access_token import generate_access_token
from auth.jwt.access_token.decode_access_token import decode_access_token
from auth.jwt.access_token.ban_access_token import ban_access_token


def database_process(
    data_base: database_dependency, user: User, access_token: str
):
    user_information = data_base.query(JWTList).filter_by(user_id=user.id).first()

    access_token_payload = decode_access_token(access_token)
    access_token_uuid = access_token_payload.get("uuid")
    expired_date_access_token_unix_timestamp = access_token_payload.get("exp")

    if user_information:
        user_information.access_token_uuid = access_token_uuid
        user_information.access_token_unix_timestamp = (
            expired_date_access_token_unix_timestamp
        )
        data_base.add(user_information)
        data_base.commit()
        
        return True

    return False

def reissue_access_token(
    data_base: database_dependency,
    refresh_token_payload: current_user_refresh_token_payload,
):
    user = data_base.query(User).filter_by(id=refresh_token_payload.get("user_id")).first()

    ban_access_token(data_base=data_base, user_id=user.id)
    access_token = generate_access_token(data_base=data_base, user=user)
    database_process(
        data_base=data_base,
        user=user,
        access_token=access_token
    )

    # return의 dict는 차후 dto로 변경한다.

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
