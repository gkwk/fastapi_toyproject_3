from fastapi import Path

from database.database import database_dependency
from models import Comment
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def get_comments(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
    post_id: int,
):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    fileter_kwargs = {"post_id": post_id}

    return {
        "role": token.get("role"),
        "comments": data_base.query(Comment).filter_by(**fileter_kwargs).all(),
    }


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시글의 댓글 목록을 조회한다.
    """
    return get_comments(
        data_base=data_base, token=token, board_id=board_id, post_id=post_id
    )
