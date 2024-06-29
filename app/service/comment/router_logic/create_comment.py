import uuid
from typing import cast

from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message import http_exception_params
from exception_message.sql_exception_messages import integrity_exception_messages
from models import CommentFile
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.comments.request_comment_create import RequestCommentCreate
from service.comment.logic_create_comment import logic_create_comment
from service.post.logic_get_post import logic_get_post
from service.board.logic_get_board import logic_get_board


def create_comment(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestCommentCreate,
    board_id: int,
    post_id: int,
):
    board = logic_get_board(data_base=data_base, filter_dict={"id": board_id})
    post = logic_get_post(
        data_base=data_base, filter_dict={"id": post_id, "board_id": board_id}
    )

    if (not board) or (not board.is_available) or (not post):
        raise HTTPException(**http_exception_params.not_exist_resource)

    is_file_attached = False

    if schema.files != None:
        for idx, file in enumerate(schema.files):
            if file != None:
                is_file_attached = True
                break

    comment = logic_create_comment(
        data_base=data_base,
        token=token,
        post_id=post_id,
        content=schema.content,
        is_visible=schema.is_visible,
        is_file_attached=is_file_attached,
    )

    data_base.add(comment)

    try:
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    if schema.files != None:
        for idx, file in enumerate(schema.files):
            if file != None:
                file: UploadFile = cast(UploadFile, file)

                file_uuid_name = str(uuid.uuid4())
                file_path = (
                    f"volume/staticfile/comment_{file_uuid_name}_{file.filename}"
                )
                with open(file_path, "wb+") as file_object:
                    file_object.write(file.file.read())
                    comment_file = CommentFile(
                        comment_id=comment.id,
                        post_id=post_id,
                        file_uuid_name=file_uuid_name,
                        file_original_name=file.filename,
                        file_path=file_path,
                    )
                    data_base.add(comment_file)
        try:
            data_base.commit()

        except IntegrityError as e:
            data_base.rollback()

            error_code = intergrity_error_message_parser.parsing(
                integrity_error_message_orig=e.orig
            )
            raise HTTPException(**integrity_exception_messages(error_code))

    return comment
