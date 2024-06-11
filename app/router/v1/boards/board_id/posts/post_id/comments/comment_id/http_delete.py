from fastapi import HTTPException, Path
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.posts.post_id.comments.comment_id.router import router
from database.database import database_dependency
from models import Comment
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message.http_exception_params import http_exception_params


def delete_comment(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
    post_id: int,
    comment_id: int,
):
    comment = data_base.query(Comment).filter_by(id=comment_id, post_id=post_id).first()

    if token.get("user_id") != comment.user_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    data_base.delete(comment)
    data_base.commit()


@router.delete(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.COMMENT_TAG]
)
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
    delete_comment(
        data_base=data_base,
        token=token,
        board_id=board_id,
        post_id=post_id,
        comment_id=comment_id,
    )
