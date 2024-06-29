import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy import select, delete, and_
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.board.logic_get_board import logic_get_board
from service.post.logic_get_post import logic_get_post
from service.base_update_processor import BaseUpdateProcessor
from service.base_update_manager import BaseUpdateManager
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from models import PostFile, Post
from schema.posts.request_post_detail_patch import RequestPostDetailPatch


class _NameUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Post, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Post, key: str, value):
        model.name = value


class _ContentUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Post, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Post, key: str, value):
        model.content = value


class _IsVisibleUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Post, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Post, key: str, value):
        model.is_visible = value


class _FileListAppendProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Post, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Post, key: str, value):
        is_file_attached = model.is_file_attached

        if value is not None:
            for file in value:
                if file is not None:
                    is_file_attached = True
                    file: UploadFile
                    file_uuid_name = str(uuid.uuid4())
                    file_path = f"volume/staticfile/{file_uuid_name}_{file.filename}"
                    with open(file_path, "wb+") as file_object:
                        file_object.write(file.file.read())
                        post_file = PostFile(
                            post_id=model.id,
                            board_id=model.board_id,
                            file_uuid_name=file_uuid_name,
                            file_original_name=file.filename,
                            file_path=file_path,
                        )
                        data_base.add(post_file)
        model.is_file_attached = is_file_attached


class _FileListRemoveProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Post, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Post, key: str, value):
        get_stmt = select(PostFile.file_uuid_name).where(
            and_(PostFile.post_id == model.id, PostFile.board_id == model.board_id)
        )

        current_file_id_set = set(data_base.execute(get_stmt).scalars().all())
        remove_file_id_set = set(value) & current_file_id_set

        if remove_file_id_set:
            delete_stmt = delete(PostFile).where(
                and_(
                    PostFile.post_id == model.id,
                    PostFile.board_id == model.board_id,
                    PostFile.file_uuid_name.in_(remove_file_id_set),
                )
            )

            data_base.execute(delete_stmt)

            if len(current_file_id_set) == len(remove_file_id_set):
                model.is_file_attached = False


class _PostUpdateManager(BaseUpdateManager):
    def __init__(self):
        super().__init__()
        self.update_validation_classes["name"] = _NameUpdateProcessor()
        self.update_validation_classes["content"] = _ContentUpdateProcessor()
        self.update_validation_classes["is_visible"] = _IsVisibleUpdateProcessor()
        self.update_validation_classes["file_list_append"] = _FileListAppendProcessor()
        self.update_validation_classes["file_list_remove"] = _FileListRemoveProcessor()


_post_update_manager = _PostUpdateManager()


def update_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestPostDetailPatch,
    board_id: int,
    post_id: int,
):
    try:
        filter_dict = {"id": board_id}
        board = logic_get_board(data_base=data_base, filter_dict=filter_dict)

        filter_dict = {"id": post_id, "board_id": board_id}
        if token.role != "ROLE_ADMIN":
            filter_dict["user_id"] = token.user_id

        post = logic_get_post(
            data_base=data_base,
            filter_dict=filter_dict,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )

    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if (not board) or (not board.is_available) or (not post):
        raise HTTPException(**http_exception_params.not_exist_resource)

    schema_dump = schema.model_dump(exclude_unset=True)

    for key, value in schema_dump.items():
        _post_update_manager.update(
            data_base=data_base, model=post, key=key, value=value
        )

    data_base.add(post)

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()
        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
