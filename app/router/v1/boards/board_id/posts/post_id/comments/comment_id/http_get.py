from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.comment.router_logic.get_comment_detail import get_comment_detail
from auth.jwt.scope_checker import scope_checker
from database.redis_method import board_cache_get


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

    if not board_cache_get(board_id=board_id):
        scope_checker(target_scopes=[board_id], token=token)

    try:
        comment = get_comment_detail(
            data_base=data_base,
            post_id=post_id,
            comment_id=comment_id,
        )

        file_name_list = []

        for file in comment.attached_files:
            file_name_list.append(file.file_path.split("/")[-1])

    except HTTPException as e:
        raise e

    return {
        "role": token.role,
        "detail": comment,
        "file_name_list": file_name_list,
    }
