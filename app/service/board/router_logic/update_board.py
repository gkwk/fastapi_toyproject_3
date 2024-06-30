from fastapi import HTTPException
from sqlalchemy import select, delete, insert, and_
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from database.cache import board_cache_set
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.base_update_processor import BaseUpdateProcessor
from service.base_update_manager import BaseUpdateManager
from service.board.logic_get_board import logic_get_board
from models import Board, UserPermissionTable, JWTList, JWTAccessTokenBlackList
from schema.boards.request_board_detail_patch import RequestBoardDetailPatch
from auth.jwt.access_token.ban_access_token import ban_access_token


class _NameUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Board, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Board, key: str, value):
        model.name = value


class _InformationUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Board, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Board, key: str, value):
        model.information = value


class _IsVisibleUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Board, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Board, key: str, value):
        model.is_visible = value


class _IsAvailableUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Board, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Board, key: str, value):
        model.is_available = value


class _UserListPermissionAppendProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Board, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Board, key: str, value):
        get_stmt = select(UserPermissionTable.user_id).where(
            UserPermissionTable.board_id == model.id
        )
        current_permission_user_ids = set(
            data_base.execute(statement=get_stmt).scalars().all()
        )

        new_permission_user_ids = set(value) - current_permission_user_ids

        # 차후 등록된 user의 id를 넘는 것을 제외하는 기능을 추가한다.
        # 방법 -> set를 검사해서 최대 user_id를 넘는 것을 보관하는 set를 추가로 생성한다. 이후 new_permission_user_ids에서 생성된 set를 뺀다.

        if new_permission_user_ids:
            insert_stmt = insert(UserPermissionTable).values(
                [
                    {"board_id": model.id, "user_id": user_id}
                    for user_id in new_permission_user_ids
                ]
            )

            data_base.execute(insert_stmt)

            for user_id in new_permission_user_ids:
                # 차후 timeout 등을 사용하는 법을 찾아본다.
                jwt = (
                    data_base.query(JWTList)
                    .filter_by(user_id=user_id)
                    .limit(1)
                    .with_for_update(nowait=True, skip_locked=True)
                    .first()
                )

                if (
                    (jwt is not None)
                    and (jwt.access_token_uuid is not None)
                    and (jwt.access_token_unix_timestamp is not None)
                ):
                    blacklisted_access_token = (
                        data_base.query(JWTAccessTokenBlackList)
                        .filter_by(
                            user_id=user_id,
                            access_token_uuid=jwt.access_token_uuid,
                            access_token_unix_timestamp=jwt.access_token_unix_timestamp,
                        )
                        .limit(1)
                        .with_for_update(nowait=True, skip_locked=True)
                        .first()
                    )
                else:
                    blacklisted_access_token = None

                if jwt:
                    ban_access_token(
                        data_base=data_base,
                        jwt=jwt,
                        blacklisted_access_token=blacklisted_access_token,
                    )


class _UserListPermissionRemoveProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: Board, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: Board, key: str, value):
        get_stmt = select(UserPermissionTable.user_id).where(
            UserPermissionTable.board_id == model.id
        )
        current_permission_user_ids = set(
            data_base.execute(statement=get_stmt).scalars().all()
        )

        remove_permission_user_ids = set(value) & current_permission_user_ids

        if remove_permission_user_ids:
            stmt = delete(UserPermissionTable).where(
                and_(
                    UserPermissionTable.board_id == model.id,
                    UserPermissionTable.user_id.in_(remove_permission_user_ids),
                )
            )
            data_base.execute(stmt)

            for user_id in remove_permission_user_ids:
                # 차후 timeout 등을 사용하는 법을 찾아본다.
                jwt = (
                    data_base.query(JWTList)
                    .filter_by(user_id=user_id)
                    .limit(1)
                    .with_for_update(nowait=True, skip_locked=True)
                    .first()
                )

                if (
                    (jwt is not None)
                    and (jwt.access_token_uuid is not None)
                    and (jwt.access_token_unix_timestamp is not None)
                ):
                    blacklisted_access_token = (
                        data_base.query(JWTAccessTokenBlackList)
                        .filter_by(
                            user_id=user_id,
                            access_token_uuid=jwt.access_token_uuid,
                            access_token_unix_timestamp=jwt.access_token_unix_timestamp,
                        )
                        .limit(1)
                        .with_for_update(nowait=True, skip_locked=True)
                        .first()
                    )
                else:
                    blacklisted_access_token = None

                if jwt:
                    ban_access_token(
                        data_base=data_base,
                        jwt=jwt,
                        blacklisted_access_token=blacklisted_access_token,
                    )


class _BoardUpdateManager(BaseUpdateManager):
    def __init__(self):
        super().__init__()
        self.update_validation_classes["name"] = _NameUpdateProcessor()
        self.update_validation_classes["information"] = _InformationUpdateProcessor()
        self.update_validation_classes["is_visible"] = _IsVisibleUpdateProcessor()
        self.update_validation_classes["is_available"] = _IsAvailableUpdateProcessor()
        self.update_validation_classes["user_list_permission_append"] = (
            _UserListPermissionAppendProcessor()
        )
        self.update_validation_classes["user_list_permission_remove"] = (
            _UserListPermissionRemoveProcessor()
        )


_board_update_manager = _BoardUpdateManager()


def update_board_detail(
    data_base: database_dependency,
    schema: RequestBoardDetailPatch,
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

    schema_dump = schema.model_dump(exclude_unset=True)

    for key, value in schema_dump.items():
        _board_update_manager.update(
            data_base=data_base, model=board, key=key, value=value
        )

    data_base.add(board)

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()
        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
    
    board_cache_set(board_id=board_id, is_visible=board.is_visible)
