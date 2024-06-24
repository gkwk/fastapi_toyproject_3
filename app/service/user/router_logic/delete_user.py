from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from auth.jwt.access_token.ban_access_token import ban_access_token
from auth.jwt.refresh_token.delete_refresh_token import delete_refresh_token
from exception_message import http_exception_params
from exception_message.sql_exception_messages import integrity_exception_messages
from service.user.logic_get_user_with_id import logic_get_user_with_id
from models import JWTList, JWTAccessTokenBlackList


# def _get_jwt(data_base: database_dependency, user_id: int):
#     try:
#         jwt = (
#             data_base.query(JWTList)
#             .filter_by(user_id=user_id)
#             .limit(1)
#             .with_for_update(nowait=True)
#             .first()
#         )
#     except OperationalError as e:
#         raise HTTPException(status_code=400)

#     return jwt

# def _get_blacklisted_access_token(
#     data_base: database_dependency, user_id: int, user_jwt_information: JWTList
# ):
#     try:
#         blacklisted_access_token = (
#             data_base.query(JWTAccessTokenBlackList)
#             .filter_by(
#                 user_id=user_id,
#                 access_token_uuid=user_jwt_information.access_token_uuid,
#                 access_token_unix_timestamp=user_jwt_information.access_token_unix_timestamp,
#             )
#             .limit(1)
#             .with_for_update(nowait=True)
#             .first()
#         )
#     except OperationalError as e:
#         raise HTTPException(status_code=400)

#     return blacklisted_access_token


def delete_user(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    user_id: int,
):
    if token.user_id != user_id:
        raise HTTPException(**http_exception_params.not_verified_token)

    user = logic_get_user_with_id(data_base=data_base, user_id=token.user_id)

    if user is None:
        raise HTTPException(**http_exception_params.not_exist_user)

    try:
        jwt = (
            data_base.query(JWTList)
            .filter_by(user_id=user.id)
            .limit(1)
            .with_for_update(nowait=True)
            .first()
        )
        if (jwt.access_token_uuid is not None) and (
            jwt.access_token_unix_timestamp is not None
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

    except OperationalError as e:
        raise HTTPException(status_code=400)

    data_base.delete(user)
    # jwt list를 통해 refresh token과 access token을 삭제한다.
    ban_access_token(
        data_base=data_base,
        jwt=jwt,
        blacklisted_access_token=blacklisted_access_token,
    )
    delete_refresh_token(data_base=data_base, jwt=jwt)

    try:
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
