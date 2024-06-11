from typing import Union

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.router import router
from database.database import database_dependency
from models import Board
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.boards.response_board_detail import (
    ResponseBoardDetailForUser,
    ResponseBoardDetailForAdmin,
)


def get_board_detail(
    data_base: database_dependency, token: current_user_access_token_payload, board_id: int
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.
    return {
        "role": token.get("role"),
        "detail": data_base.query(Board).filter_by(id=board_id).one(),
    }


@router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseBoardDetailForUser, ResponseBoardDetailForAdmin],tags=[v1_tags.BOARD_TAG]
)
def http_get(
    data_base: database_dependency, token: current_user_access_token_payload, board_id: int
):
    """
    게시판 정보를 조회한다.
    """
    return get_board_detail(data_base=data_base, token=token, board_id=board_id)
