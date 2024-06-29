from fastapi import Path, HTTPException

from database.database import database_dependency
from models import PostViewIncrement
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)

from service.post.router_logic.get_post_detail import get_post_detail

from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message.sql_exception_messages import integrity_exception_messages
from sqlalchemy.exc import IntegrityError


def record_post_view(data_base: database_dependency, post_id: int):
    post_view_increment: PostViewIncrement = PostViewIncrement(
        post_id=post_id,
    )
    data_base.add(post_view_increment)

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시판의 게시글 정보를 조회한다.
    """

    try:
        post = get_post_detail(
            data_base=data_base,
            board_id=board_id,
            post_id=post_id,
            user_role=token.role,
        )
        record_post_view(data_base=data_base, post_id=post_id)

    except HTTPException as e:
        raise e

    return {"role": token.role, "detail": post}
