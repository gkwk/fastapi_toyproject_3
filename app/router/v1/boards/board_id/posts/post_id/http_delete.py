from fastapi import HTTPException, Path
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.posts.post_id.router import router
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


@router.delete(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.POST_TAG]
)
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
