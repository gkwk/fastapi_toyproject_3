import secrets

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency, DATABASE_DRIVER_NAME
from database.integrity_error_message_parser import intergrity_error_message_parser
from models import User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from auth.jwt.password_context import get_password_context
from schema.users.request_user_detail_patch import RequestUserDetailPatch
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.base_update_processor import BaseUpdateProcessor
from service.base_update_manager import BaseUpdateManager
from service.user.logic_get_user_with_email import logic_get_user_with_email
from service.user.logic_get_user_with_id import logic_get_user_with_id


class _EmailUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: User, key: str, value):
        # if logic_get_user_with_email(data_base=data_base, email=value) is not None:
        #     raise HTTPException(**http_exception_params.not_unique_email)
        pass

    def set_value(self, data_base: database_dependency, model: User, key: str, value):
        model.email = value


class _PasswordUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: User, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: User, key: str, value):
        generated_password_salt = secrets.token_hex(4)
        model.password = get_password_context().hash(value + generated_password_salt)
        model.password_salt = generated_password_salt


class _UserUpdateManager(BaseUpdateManager):
    def __init__(self):
        super().__init__()
        self.update_validation_classes["email"] = _EmailUpdateProcessor()
        self.update_validation_classes["password1"] = _PasswordUpdateProcessor()


_user_update_manager = _UserUpdateManager()


def update_user(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestUserDetailPatch,
    user_id: int,
):
    if token.user_id != user_id:
        raise HTTPException(**http_exception_params.not_verified_token)

    try:
        user = logic_get_user_with_id(
            data_base=data_base,
            user_id=user_id,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )
    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if user is None:
        raise HTTPException(**http_exception_params.not_exist_user)

    schema_dump = schema.model_dump(exclude_unset=True)

    for key, value in schema_dump.items():
        _user_update_manager.update(
            data_base=data_base, model=user, key=key, value=value
        )

    try:
        data_base.add(user)
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    # 차후 access token 재발행 여부를 묻는 과정의 추가를 고려한다.
