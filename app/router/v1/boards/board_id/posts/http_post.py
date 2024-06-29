from fastapi import Depends, Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.posts.request_post_create import RequestFormPostCreate, RequestPostCreate
from service.post.router_logic.create_post import create_post


def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestPostCreate = Depends(RequestFormPostCreate.from_form),
    board_id: int = Path(ge=1),
):
    """
    게시글을 생성한다.
    """

    try:
        post = create_post(
            data_base=data_base, token=token, schema=schema, board_id=board_id
        )
    except HTTPException as e:
        raise e

    return {"result": "success", "id": post.id}
