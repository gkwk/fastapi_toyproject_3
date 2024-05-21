from typing import Union

from fastapi import Path, HTTPException

from router.v1 import v1_url, v1_tags
from router.v1.boards.id.posts.post_id.comments.comment_id.router import router
from database.database import database_dependency
from models import Comment
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.comments.response_post_detail import (
    ResponseCommentDetailForUser,
    ResponseCommentDetailForAdmin,
)
from exception_message.http_exception_params import http_exception_params


def get_comment_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
    post_id: int,
    comment_id: int,
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.
    # Comment에 board_id를 나중에 추가하여 board_id를 filter로 사용한다.

    comment = data_base.query(Comment).filter_by(id=comment_id, post_id=post_id).first()

    if not comment:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    return {
        "role": token.get("role"),
        "detail": comment,
    }


@router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseCommentDetailForUser, ResponseCommentDetailForAdmin],
    tags=[v1_tags.COMMENT_TAG],
)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
    comment_id: int = Path(ge=1),
):
    """
    게시글의 댓글을 조회한다.
    """
    return get_comment_detail(
        data_base=data_base,
        token=token,
        board_id=board_id,
        post_id=post_id,
        comment_id=comment_id,
    )
