from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from models import JWTAccessTokenBlackList, JWTList
from database.database import database_dependency


# def get_jwt(data_base: database_dependency, user_id: int):
#     try:
#         jwt = data_base.query(JWTList).filter_by(user_id=user_id).limit(1).first()
#     except OperationalError as e:
#         raise HTTPException(status_code=400)

#     return jwt


# def get_blacklisted_access_token(
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


def ban_access_token(
    data_base: database_dependency,
    jwt: JWTList | None,
    blacklisted_access_token: JWTAccessTokenBlackList | None,
):
    if (
        (jwt is not None)
        and (jwt.access_token_uuid is not None)
        and (jwt.access_token_unix_timestamp is not None)
    ):
        # refresh token으로 access token이 발행되었는지 확인한다.

        if blacklisted_access_token is None:
            # 기존의 access token이 블랙리스트에 기록되지 않은 것을 확인한다.

            # 블랙리스트에 access token을 기록한다.
            new_blacklisted_access_token = JWTAccessTokenBlackList(
                user_id=jwt.user_id,
                access_token_uuid=jwt.access_token_uuid,
                access_token_unix_timestamp=jwt.access_token_unix_timestamp,
            )

            # 트랜잭션에 추가한다.
            data_base.add(new_blacklisted_access_token)


# token ban 과정에서 다른 ban 과정이 진행될 수 있으므로, 이를 위한 예외처리를 추가한다.
