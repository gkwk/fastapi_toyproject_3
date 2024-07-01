from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from models import JWTList
from database.database import database_dependency
from database.cache import (
    blacklisted_access_token_cache_set,
    blacklisted_access_token_cache_exist,
)


def ban_access_token(data_base: database_dependency, jwt: JWTList | None):
    # Redis 관련 예외처리 추가를 고려한다.

    if jwt is not None:
        # 기존의 access token이 블랙리스트에 기록되지 않은 것을 확인한다.
        if not blacklisted_access_token_cache_exist(
            user_id=jwt.user_id,
            uuid=jwt.access_token_uuid,
            timestamp=jwt.access_token_unix_timestamp,
        ):
            blacklisted_access_token_cache_set(
                user_id=jwt.user_id,
                uuid=jwt.access_token_uuid,
                timestamp=jwt.access_token_unix_timestamp,
            )
