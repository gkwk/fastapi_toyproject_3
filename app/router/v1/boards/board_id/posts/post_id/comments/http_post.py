from fastapi import Depends, Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.comments.request_comment_create import (
    RequestFormCommentCreate,
    RequestCommentCreate,
)
from service.comment.router_logic.create_comment import create_comment


def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestCommentCreate = Depends(RequestFormCommentCreate.from_form),
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시글의 댓글을 생성한다.
    """

    try:
        comment = create_comment(
            data_base=data_base,
            token=token,
            schema=schema,
            board_id=board_id,
            post_id=post_id,
        )
    except HTTPException as e:
        raise e

    return {"result": "success", "id": comment.id}
