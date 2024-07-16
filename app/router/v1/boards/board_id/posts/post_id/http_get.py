from uuid import uuid4
from time import time

from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)

from service.post.router_logic.get_post_detail import get_post_detail

from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message.sql_exception_messages import integrity_exception_messages
from sqlalchemy.exc import IntegrityError

from auth.jwt.scope_checker import scope_checker
from database.redis_method import board_cache_get, post_view_count_cache_set


def record_post_view(
    data_base: database_dependency,
    user_id: int,
    post_id: int,
):
    uuid = str(uuid4())
    timestamp = int(time())
    try:
        post_view_count_cache_set(
            user_id=user_id, post_id=post_id, uuid=uuid, timestamp=timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500)


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시판의 게시글 정보를 조회한다.
    """

    if not board_cache_get(board_id=board_id):
        scope_checker(target_scopes=[board_id], token=token)

    try:
        post = get_post_detail(
            data_base=data_base,
            board_id=board_id,
            post_id=post_id,
            user_role=token.role,
        )
        record_post_view(data_base=data_base, user_id=token.user_id, post_id=post_id)

    except HTTPException as e:
        raise e

    return {"role": token.role, "detail": post}
