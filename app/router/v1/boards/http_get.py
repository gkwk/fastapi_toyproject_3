from database.database import database_dependency
from models import Board
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def get_boards(
    data_base: database_dependency, token: current_user_access_token_payload
):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    return {
        "role": token.get("role"),
        "boards": data_base.query(Board).filter_by().all(),
    }


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    게시판 목록을 조회한다.
    """
    return get_boards(data_base=data_base, token=token)
