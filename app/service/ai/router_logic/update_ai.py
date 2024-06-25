from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from models import AI
from schema.ais.request_ai_detail_patch import RequestAIDetailPatch
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.base_update_processor import BaseUpdateProcessor
from service.base_update_manager import BaseUpdateManager
from service.ai.logic_get_ai import logic_get_ai
from service.ai.logic_get_ai_with_id import logic_get_ai_with_id


class _NameUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: AI, key: str, value):
        pass
    
    def set_value(self, data_base: database_dependency, model: AI, key: str, value):
        model.name = value


class _DescriptionUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: AI, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: AI, key: str, value):
        model.description = value


class _IsVisibleUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: AI, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: AI, key: str, value):
        model.is_visible = value


class _IsAvailableUpdateProcessor(BaseUpdateProcessor):
    def validate(self, data_base: database_dependency, model: AI, key: str, value):
        pass

    def set_value(self, data_base: database_dependency, model: AI, key: str, value):
        model.is_available = value


class _AIUpdateManager(BaseUpdateManager):
    def __init__(self):
        super().__init__()
        self.update_validation_classes["name"] = _NameUpdateProcessor()
        self.update_validation_classes["description"] = _DescriptionUpdateProcessor()
        self.update_validation_classes["is_visible"] = _IsVisibleUpdateProcessor()
        self.update_validation_classes["is_available"] = _IsAvailableUpdateProcessor()


_ai_update_manager = _AIUpdateManager()


def update_ai_detail(
    data_base: database_dependency,
    schema: RequestAIDetailPatch,
    ai_id: int,
):
    try:
        ai = logic_get_ai_with_id(
            data_base=data_base,
            ai_id=ai_id,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )
    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if ai is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    # key가 없는 속성값은 제거한다. 이를 통해 None을 NULL값으로 사용할 수 있게된다.
    schema_dump = schema.model_dump(exclude_unset=True)

    # is_visible, is_available이 수정되면 사용자 접근 권한을 초기화하고, permission_verified_user_id_range을 0으로 바꾸는 함수를 차후 추가한다.
    for key, value in schema_dump.items():
        _ai_update_manager.update(data_base=data_base, model=ai, key=key, value=value)

    data_base.add(ai)

    try:
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
