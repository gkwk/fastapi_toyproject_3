from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.board.router_logic.get_board_detail import get_board_detail


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    """
    게시판 정보를 조회한다.
    """
    try:
        board = get_board_detail(
            data_base=data_base, board_id=board_id, user_role=token.role
        )
    except HTTPException as e:
        raise e

    return {"role": token.role, "detail": board}
