from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.post.router_logic.get_posts import get_posts


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
):
    """
    게시글 목록을 조회한다.
    """
    try:
        posts = get_posts(data_base=data_base, board_id=board_id, user_role=token.role)
    except HTTPException as e:
        raise e

    return {"role": token.role, "posts": posts}
