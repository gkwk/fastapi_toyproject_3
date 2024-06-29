from fastapi import HTTPException, Depends, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.comments.request_comment_detail_patch import (
    RequestCommentDetailPatch,
    RequestFormCommentDetailPatch,
)
from service.comment.router_logic.update_comment import update_comment


def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestCommentDetailPatch = Depends(
        RequestFormCommentDetailPatch.to_pydantic
    ),
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
    comment_id: int = Path(ge=1),
):
    """
    게시글의 댓글 상세 정보를 수정한다.
    """
    try:
        update_comment(
            data_base=data_base,
            token=token,
            schema=schema,
            board_id=board_id,
            post_id=post_id,
            comment_id=comment_id,
        )
    except HTTPException as e:
        raise e
