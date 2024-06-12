from fastapi import Path, HTTPException

from database.database import database_dependency
from models import Post, PostViewIncrement
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)

from exception_message.http_exception_params import http_exception_params


def get_post_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
    post_id: int,
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.

    post = data_base.query(Post).filter_by(id=post_id, board_id=board_id).first()

    if not post:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    return {
        "role": token.get("role"),
        "detail": post,
    }


def record_post_view(data_base: database_dependency, post_id: int):
    post_view_increment: PostViewIncrement = PostViewIncrement(
        post_id=post_id,
    )
    data_base.add(post_view_increment)
    data_base.commit()


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시판의 게시글 정보를 조회한다.
    """
    record_post_view(data_base=data_base, post_id=post_id)

    return get_post_detail(
        data_base=data_base, token=token, board_id=board_id, post_id=post_id
    )
