import secrets

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from models import User
from auth.jwt.password_reset_token.get_user_password_reset_token_payload import (
    current_user_password_reset_token_payload,
)
from auth.jwt.password_context import get_password_context
from schema.password_reset.request_user_password_reset import RequestUserPasswordReset
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.base_update_processor import BaseUpdateProcessor
from service.base_update_manager import BaseUpdateManager
from service.user.logic_get_user_with_id import logic_get_user_with_id

from database.redis_method import (
    password_reset_token_cache_exist,
    password_reset_token_cache_unlink,
)


class _PasswordUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: User, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: User, key: str, value):
        generated_password_salt = secrets.token_hex(4)
        model.password = get_password_context().hash(value + generated_password_salt)
        model.password_salt = generated_password_salt


class _PasswordResetManager(BaseUpdateManager):
    def __init__(self):
        super().__init__()
        self.update_validation_classes["password1"] = _PasswordUpdateProcessor()


_password_reset_manager = _PasswordResetManager()


def password_reset(
    data_base: database_dependency,
    token: current_user_password_reset_token_payload,
    schema: RequestUserPasswordReset,
):
    if not password_reset_token_cache_exist(
        user_id=token.user_id, uuid=token.uuid, timestamp=token.exp
    ):
        raise HTTPException(**http_exception_params.not_verified_token)

    try:
        user = logic_get_user_with_id(
            data_base=data_base,
            user_id=token.user_id,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )
    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if user is None:
        raise HTTPException(**http_exception_params.not_exist_user)

    password_reset_token_cache_unlink(
        user_id=token.user_id, uuid=token.uuid, timestamp=token.exp
    )

    schema_dump = schema.model_dump(exclude_unset=True)

    for key, value in schema_dump.items():
        _password_reset_manager.update(
            data_base=data_base, model=user, key=key, value=value
        )

    try:
        # password_reset_token_cache_exist나 password_reset_token_cache_unlink를 이곳에도 추가하거나 옮기는 것을 고려해본다.
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    # 차후 access token 재발행 여부를 묻는 과정의 추가를 고려한다.
