from fastapi import HTTPException, Depends, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.posts.request_post_detail_patch import (
    RequestFormPostDetailPatch,
    RequestPostDetailPatch,
)
from service.post.router_logic.update_post import update_post


def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestPostDetailPatch = Depends(RequestFormPostDetailPatch.to_pydantic),
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시판의 게시글 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    try:
        update_post(
            data_base=data_base,
            token=token,
            schema=schema,
            board_id=board_id,
            post_id=post_id,
        )
    except HTTPException as e:
        raise e
