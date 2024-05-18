import uuid
from typing import cast

from starlette import status
from fastapi import Depends, Path, HTTPException, UploadFile

from router.v1 import v1_url, v1_tags
from router.v1.boards.id.posts.router import router
from database.database import database_dependency
from models import Post, Board, PostFile
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.posts.request_post_create import RequestFormPostCreate
from exception_message.http_exception_params import http_exception_params


def create_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestFormPostCreate,
    board_id: int,
):
    board = data_base.query(Board).filter_by(id=board_id).first()

    if not board:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    is_file_attached = False

    if schema.files != None:
        for idx, file in enumerate(schema.files):
            if file != None:
                is_file_attached = True
                break

    post = Post(
        user_id=token.get("user_id"),
        board_id=board_id,
        name=schema.name,
        content=schema.content,
        is_visible=schema.is_visible,
        is_file_attached=is_file_attached,
    )

    data_base.add(post)
    data_base.commit()

    if schema.files != None:
        for idx, file in enumerate(schema.files):
            if file != None:
                file: UploadFile = cast(UploadFile, file)

                file_uuid_name = str(uuid.uuid4())
                file_path = f"volume/staticfile/{file_uuid_name}_{file.filename}"
                with open(file_path, "wb+") as file_object:
                    file_object.write(file.file.read())
                    post_file = PostFile(
                        post_id=post.id,
                        board_id=board_id,
                        file_uuid_name=file_uuid_name,
                        file_original_name=file.filename,
                        file_path=file_path,
                    )
                    data_base.add(post_file)
        data_base.commit()

    return post.id


@router.post(
    v1_url.ENDPOINT, status_code=status.HTTP_201_CREATED, tags=[v1_tags.POST_TAG]
)
def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestFormPostCreate = Depends(RequestFormPostCreate.from_form),
    board_id: int = Path(ge=1),
):
    """
    게시글을 생성한다.
    """
    post_id = create_post(
        data_base=data_base, token=token, schema=schema, board_id=board_id
    )

    return {"result": "success", "id": post_id}
