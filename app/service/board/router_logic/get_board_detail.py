from fastapi import HTTPException

from database.database import database_dependency
from exception_message import http_exception_params
from service.board.logic_get_board import logic_get_board


def get_board_detail(
    data_base: database_dependency,
    board_id: int,
    user_role: str,
):
    filter_dict = {"id": board_id}

    if user_role != "ROLE_ADMIN":
        filter_dict["is_available"] = True

    board = logic_get_board(data_base=data_base, filter_dict=filter_dict)

    if board is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    return board
