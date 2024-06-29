from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.post.router_logic.delete_post import delete_post


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시판의 게시글을 삭제한다.
    """
    try:
        delete_post(
            data_base=data_base, token=token, board_id=board_id, post_id=post_id
        )

    except HTTPException as e:
        raise e
