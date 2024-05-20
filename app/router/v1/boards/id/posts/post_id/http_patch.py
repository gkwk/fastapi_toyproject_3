from typing import cast
import uuid

from fastapi import HTTPException, UploadFile, Depends, Path
from starlette import status
from sqlalchemy import select

from router.v1 import v1_url, v1_tags
from router.v1.boards.id.posts.post_id.router import router
from database.database import database_dependency
from models import Board, PostFile, Post
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.posts.request_post_detail_patch import (
    RequestFormPostDetailPatch,
    RequestPostDetailPatch,
)
from exception_message.http_exception_params import http_exception_params


def validate_before_set_value(key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.
    pass


def set_value(post: Post, key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.

    if key == "file_list_append":
        is_file_attached = post.is_file_attached

        if value != None:
            for idx, file in enumerate(value):
                if file != None:
                    is_file_attached = True

                    file: UploadFile = cast(UploadFile, file)

                    file_uuid_name = str(uuid.uuid4())
                    file_path = f"volume/staticfile/{file_uuid_name}_{file.filename}"
                    with open(file_path, "wb+") as file_object:
                        file_object.write(file.file.read())
                        post_file = PostFile(
                            post_id=post.id,
                            board_id=post.board_id,
                            file_uuid_name=file_uuid_name,
                            file_original_name=file.filename,
                            file_path=file_path,
                        )
                        data_base.add(post_file)
            data_base.commit()
        post.is_file_attached = is_file_attached

    elif key == "file_list_remove":
        stmt = select(PostFile.file_uuid_name).where(
            PostFile.post_id == post.id, PostFile.board_id == post.board_id
        )

        already_exist_file_id_set = set(
            data_base.execute(statement=stmt).scalars().all()
        )

        remove_file_id_set = set(value) & already_exist_file_id_set

        stmt = select(PostFile).where(
            PostFile.post_id == post.id,
            PostFile.board_id == post.board_id,
            PostFile.file_uuid_name.in_(remove_file_id_set),
        )

        # uuid4의 중복 가능성은 매우 희박하지만, 중복 발생 확률이 0은 아니므로 uuid의 중복을 해결할 방법도 고려해야 한다.
        # 리스트내 파일의 삭제보다는 파일의 가시성을 조절하는 방법을 고려하는 것도 좋을 듯 하다.
        files = data_base.execute(statement=stmt).scalars().all()

        for file in files:
            data_base.delete(file)

        if len(already_exist_file_id_set) == len(remove_file_id_set):
            post.is_file_attached = False


def update_post_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestPostDetailPatch,
    board_id: int,
    post_id: int,
):
    board = data_base.query(Board).filter_by(id=board_id).first()
    post = data_base.query(Post).filter_by(id=post_id, board_id=board_id).first()

    if (not board) or (not post):
        raise HTTPException(**http_exception_params["not_exist_resource"])

    if token.get("user_id") != post.user_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    # key가 없는 속성값은 제거한다. 이를 통해 None을 NULL값으로 사용할 수 있게된다.
    schema_dump = schema.model_dump(exclude_unset=True)

    # validation 함수와 setattr을 이용하여 속성값 변경 코드를 간단하게 표현하였다.
    # hasattr를 사용하여 속성이 없다면 개별적인 과정을 사용한다.
    # is_visible, is_available이 수정되면 사용자 접근 권한을 초기화하고, permission_verified_user_id_range을 0으로 바꾸는 함수를 차후 추가한다.
    for key, value in schema_dump.items():
        validate_before_set_value(key=key, value=value, data_base=data_base)
        if hasattr(post, key):
            setattr(post, key, value)
        else:
            set_value(post, key, value, data_base=data_base)

    data_base.add(post)
    data_base.commit()


@router.patch(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.POST_TAG]
)
def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestPostDetailPatch = Depends(RequestFormPostDetailPatch.to_pydantic),
    board_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    """
    게시판 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    update_post_detail(
        data_base=data_base,
        token=token,
        schema=schema,
        board_id=board_id,
        post_id=post_id,
    )
