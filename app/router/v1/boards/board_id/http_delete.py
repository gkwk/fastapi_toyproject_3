from fastapi import HTTPException

from database.database import database_dependency
from models import Board
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message.http_exception_params import http_exception_params


def delete_board(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    # 차후 scope 등으로 변경한다.
    if token.get("role") != "ROLE_ADMIN":
        raise HTTPException(**http_exception_params["not_verified_token"])

    board = data_base.query(Board).filter_by(id=board_id).first()

    data_base.delete(board)
    data_base.commit()


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    """
    게시판을 삭제한다.
    """
    delete_board(data_base=data_base, token=token, board_id=board_id)
