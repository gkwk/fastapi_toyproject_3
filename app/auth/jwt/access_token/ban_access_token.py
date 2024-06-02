from datetime import timedelta, datetime, UTC
import uuid
import jwt
from jwt.exceptions import InvalidTokenError


from models import JWTAccessTokenBlackList, JWTList
from database.database import database_dependency
from config.config import get_settings


def ban_access_token(
    data_base: database_dependency,
    user_id: int,
):
    user_jwt_information = data_base.query(JWTList).filter_by(user_id=user_id).first()

    if (
        (user_jwt_information is not None)
        and (user_jwt_information.access_token_uuid is not None)
        and (user_jwt_information.access_token_unix_timestamp is not None)
    ):
        user_old_access_token = data_base.query(JWTAccessTokenBlackList).filter_by(
            user_id=user_id,
            access_token_uuid=user_jwt_information.access_token_uuid,
            access_token_unix_timestamp=user_jwt_information.access_token_unix_timestamp,
        ).first()
        
        if user_old_access_token is None:
            user_old_access_token_information = JWTAccessTokenBlackList(
                user_id=user_id,
                access_token_uuid=user_jwt_information.access_token_uuid,
                access_token_unix_timestamp=user_jwt_information.access_token_unix_timestamp,
            )

            data_base.add(user_old_access_token_information)
            data_base.commit()

    # token ban 과정에서 비동기적으로 추가 ban 과정이 진행될 수 있으므로, 이를 위한 예외처리를 추가한다.