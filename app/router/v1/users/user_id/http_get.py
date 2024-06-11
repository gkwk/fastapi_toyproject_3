from router.v1 import v1_url, v1_tags
from router.v1.users.user_id.router import router
from database.database import database_dependency
from models import User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.users.response_user_detail import ResponseUserDetail


def get_user_detail(data_base: database_dependency, user_id: int):
    # 존재하지 않는 사용자 번호를 조회하는 예외 상황에 맞는 기능을 추가해야 한다.
    
    return data_base.query(User).filter_by(id=user_id).first()


@router.get(v1_url.ENDPOINT, response_model=ResponseUserDetail,tags=[v1_tags.USER_TAG])
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    user_id: int,
):
    """
    사용자 상세 정보를 조회한다.
    """
    return get_user_detail(data_base=data_base, user_id=user_id)
