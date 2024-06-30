from fastapi import HTTPException

from database.database import database_dependency
from database.cache import board_cache_get
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.board.router_logic.get_board_detail import get_board_detail
from auth.jwt.scope_checker import scope_checker

def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    """
    게시판 정보를 조회한다.
    """
    if not board_cache_get(board_id=board_id):
        scope_checker(target_scopes=[board_id], token=token)
        
    try:
        board = get_board_detail(
            data_base=data_base, board_id=board_id, user_role=token.role
        )
    except HTTPException as e:
        raise e

    return {"role": token.role, "detail": board}
