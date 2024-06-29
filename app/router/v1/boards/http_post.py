from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.boards.request_board_create import RequestBoardCreate
from service.board.router_logic.create_board import create_board


def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestBoardCreate,
):
    """
    게시판을 생성한다.
    """

    try:
        board = create_board(
            data_base=data_base,
            name=schema.name,
            information=schema.information,
            is_visible=schema.is_visible,
            is_available=schema.is_available,
            user_id_list=schema.user_id_list,
        )
    except HTTPException as e:
        raise e

    return {"result": "success", "id": board.id}
