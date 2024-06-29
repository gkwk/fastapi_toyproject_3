from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.boards.request_board_detail_patch import RequestBoardDetailPatch
from service.board.router_logic.update_board import update_board_detail


def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestBoardDetailPatch,
    board_id: int = Path(ge=1),
):
    """
    게시판 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    try:
        update_board_detail(data_base=data_base, schema=schema, board_id=board_id)
    except HTTPException as e:
        raise e
