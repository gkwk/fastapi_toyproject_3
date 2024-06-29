from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.comment.router_logic.delete_comment import delete_comment


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
    comment_id: int = Path(ge=1),
):
    """
    게시글의 댓글을 삭제한다.
    """
    try:
        delete_comment(
            data_base=data_base,
            token=token,
            board_id=board_id,
            post_id=post_id,
            comment_id=comment_id,
        )

    except HTTPException as e:
        raise e
