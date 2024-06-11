from typing import Union

from fastapi import Path

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.posts.router import router
from database.database import database_dependency
from models import Post
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.posts.response_posts import ResponsePostsForUser, ResponsePostsForAdmin


def get_posts(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):
    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    fileter_kwargs = {"board_id": board_id}

    return {
        "role": token.get("role"),
        "posts": data_base.query(Post).filter_by(**fileter_kwargs).all(),
    }


@router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponsePostsForUser, ResponsePostsForAdmin],
    tags=[v1_tags.POST_TAG],
)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
):
    """
    게시글 목록을 조회한다.
    """
    return get_posts(data_base=data_base, token=token, board_id=board_id)
