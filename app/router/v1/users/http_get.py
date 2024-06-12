from database.database import database_dependency
from models import User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def get_users(data_base: database_dependency):
    return {"users": data_base.query(User).filter_by().all()}


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    사용자 목록을 조회한다.
    """
    return get_users(data_base=data_base)
