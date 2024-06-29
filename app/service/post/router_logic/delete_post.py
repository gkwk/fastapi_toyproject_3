from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.post.logic_get_post import logic_get_post


def delete_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
    post_id: int,
):
    try:
        filter_dict = {"id": post_id, "board_id": board_id, "user_id": token.user_id}

        post = logic_get_post(
            data_base=data_base,
            filter_dict=filter_dict,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )

    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if post is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    data_base.delete(post)

    try:
        data_base.commit()
    except IntegrityError as e:
        print(e)
        
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
