from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.board.logic_get_board import logic_get_board


def delete_board(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
):

    try:
        filter_dict = {"id": board_id}

        board = logic_get_board(
            data_base=data_base,
            filter_dict=filter_dict,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )

    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if board is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    data_base.delete(board)

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
