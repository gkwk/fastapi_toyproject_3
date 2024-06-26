from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.comment.router_logic.get_comments import get_comments


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시글의 댓글 목록을 조회한다.
    """

    try:
        comments = get_comments(data_base=data_base, post_id=post_id)
    except HTTPException as e:
        raise e

    return {"role": token.role, "comments": comments}
