from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.board.router_logic.get_boards import get_boards


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
):
    """
    게시판 목록을 조회한다.
    """
    try:
        boards = get_boards(data_base=data_base, user_role=token.role)
    except HTTPException as e:
        raise e

    return {"role": token.role, "boards": boards}
