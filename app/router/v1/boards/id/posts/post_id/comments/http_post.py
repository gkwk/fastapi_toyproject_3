import uuid
from typing import cast

from starlette import status
from fastapi import Depends, Path, HTTPException, UploadFile

from router.v1 import v1_url, v1_tags
from router.v1.boards.id.posts.post_id.comments.router import router
from database.database import database_dependency
from models import Post, Board, Comment, CommentFile
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.comments.request_comment_create import RequestFormCommentCreate
from exception_message.http_exception_params import http_exception_params


def create_comment(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestFormCommentCreate,
    board_id: int,
    post_id: int,
):
    board = data_base.query(Board).filter_by(id=board_id).first()
    post = data_base.query(Post).filter_by(id=post_id, board_id=board_id).first()

    if (not board) or (not post):
        raise HTTPException(**http_exception_params["not_exist_resource"])

    is_file_attached = False

    if schema.files != None:
        for idx, file in enumerate(schema.files):
            if file != None:
                is_file_attached = True
                break

    comment = Comment(
        user_id=token.get("user_id"),
        post_id=post_id,
        content=schema.content,
        is_visible=schema.is_visible,
        is_file_attached=is_file_attached,
    )

    data_base.add(comment)
    data_base.commit()

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
        data_base.commit()

    return comment.id


@router.post(
    v1_url.ENDPOINT, status_code=status.HTTP_201_CREATED, tags=[v1_tags.COMMENT_TAG]
)
def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestFormCommentCreate = Depends(RequestFormCommentCreate.from_form),
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시글의 댓글을 생성한다.
    """
    comment_id = create_comment(
        data_base=data_base, token=token, schema=schema, board_id=board_id, post_id=post_id
    )

    return {"result": "success", "id": comment_id}
