from database.database import database_dependency
from models import Board
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def get_board_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.
    return {
        "role": token.get("role"),
        "detail": data_base.query(Board).filter_by(id=board_id).one(),
    }


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    """
    게시판 정보를 조회한다.
    """
    return get_board_detail(data_base=data_base, token=token, board_id=board_id)
