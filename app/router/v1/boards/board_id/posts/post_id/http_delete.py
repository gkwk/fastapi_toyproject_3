from fastapi import HTTPException, Path

from database.database import database_dependency
from models import Post
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message.http_exception_params import http_exception_params


def delete_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
    post_id: int,
):
    post = data_base.query(Post).filter_by(id=post_id, board_id=board_id).first()

    if token.get("user_id") != post.user_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    data_base.delete(post)
    data_base.commit()


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시판의 게시글을 삭제한다.
    """
    delete_post(data_base=data_base, token=token, board_id=board_id, post_id=post_id)
