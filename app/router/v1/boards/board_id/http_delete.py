from fastapi import HTTPException

from database.database import database_dependency
from models import Board
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.board.router_logic.delete_board import delete_board


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    """
    게시판을 삭제한다.
    """
    try:
        delete_board(data_base=data_base, token=token, board_id=board_id)
    except HTTPException as e:
        raise e
