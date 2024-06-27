from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.base_update_processor import BaseUpdateProcessor
from service.base_update_manager import BaseUpdateManager
from service.chat_session.logic_get_chat_session import logic_get_chat_session
from models import ChatSession
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.request_chat_session_detail_patch import (
    RequestChatSessionDetailPatch,
)


class _NameUpdateProcessor(BaseUpdateProcessor):
    def validate(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        pass

    def set_value(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        model.name = value


class _InformationUpdateProcessor(BaseUpdateProcessor):
    def validate(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        pass

    def set_value(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        model.information = value


class _IsVisibleUpdateProcessor(BaseUpdateProcessor):
    def validate(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        pass

    def set_value(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        model.is_visible = value


class _IsClosedUpdateProcessor(BaseUpdateProcessor):
    def validate(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        pass

    def set_value(
        self, data_base: database_dependency, model: ChatSession, key: str, value
    ):
        model.is_closed = value


class _ChatSessionUpdateManager(BaseUpdateManager):
    def __init__(self):
        super().__init__()
        self.update_validation_classes["name"] = _NameUpdateProcessor()
        self.update_validation_classes["information"] = _InformationUpdateProcessor()
        self.update_validation_classes["is_visible"] = _IsVisibleUpdateProcessor()
        self.update_validation_classes["is_closed"] = _IsClosedUpdateProcessor()


_chat_session_update_manager = _ChatSessionUpdateManager()


def update_chat_session_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionDetailPatch,
    chat_session_id: int,
):
    try:
        filter_dict = {"id": chat_session_id}
        if token.role != "ROLE_ADMIN":
            filter_dict["user_create_id"] = token.user_id

        chat_session = logic_get_chat_session(
            data_base=data_base,
            filter_dict=filter_dict,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )
    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if chat_session is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    schema_dump = schema.model_dump(exclude_unset=True)

    for key, value in schema_dump.items():
        _chat_session_update_manager.update(
            data_base=data_base, model=chat_session, key=key, value=value
        )

    data_base.add(chat_session)

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()
        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
