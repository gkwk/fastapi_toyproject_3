from router.v1 import v1_url
from router.v1.users.router import router
from database.database import database_dependency
from models import User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.users.response_user_detail import ResponseUserDetail


def get_user_detail(data_base: database_dependency, id: int):
    return data_base.query(User).filter_by(id=id).first()


@router.get(v1_url.USERS_ID, response_model=ResponseUserDetail)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    id: int,
):
    return get_user_detail(data_base=data_base, id=id)
