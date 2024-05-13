from router.v1 import v1_url
from router.v1.users.router import router
from database.database import database_dependency
from models import User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.users.response_users import ResponseUsers


def get_users(data_base: database_dependency):
    return {"users": data_base.query(User).filter_by().all()}


@router.get(v1_url.USERS_ROOT, response_model=ResponseUsers)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    사용자 목록을 조회한다.
    """
    return get_users(data_base=data_base)
