from database.database import database_dependency
from models import AI
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def get_ais(data_base: database_dependency, token: current_user_access_token_payload):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    return {
        "role": token.get("role"),
        "ais": data_base.query(AI).filter_by().all(),
    }


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    AI 모델 목록을 조회한다.
    """
    return get_ais(data_base=data_base, token=token)
