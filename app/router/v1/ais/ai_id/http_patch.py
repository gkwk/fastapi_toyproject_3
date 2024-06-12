from typing import cast
import uuid

from fastapi import HTTPException, UploadFile, Depends, Path
from sqlalchemy import select

from database.database import database_dependency
from models import AI
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.ais.request_ai_detail_patch import RequestAIDetailPatch
from exception_message.http_exception_params import http_exception_params


def validate_before_set_value(key: str, value, data_base: database_dependency):
    if key == "name":
        if data_base.query(AI).filter_by(name=value).first():
            raise HTTPException(**http_exception_params["not_unique_attribute_value"])

    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.
    pass


def set_value(ai: AI, key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.
    pass


def update_ai_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIDetailPatch,
    ai_id: int,
):
    ai = data_base.query(AI).filter_by(id=ai_id).first()

    if not ai:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    # key가 없는 속성값은 제거한다. 이를 통해 None을 NULL값으로 사용할 수 있게된다.
    schema_dump = schema.model_dump(exclude_unset=True)

    # validation 함수와 setattr을 이용하여 속성값 변경 코드를 간단하게 표현하였다.
    # hasattr를 사용하여 속성이 없다면 개별적인 과정을 사용한다.
    # is_visible, is_available이 수정되면 사용자 접근 권한을 초기화하고, permission_verified_user_id_range을 0으로 바꾸는 함수를 차후 추가한다.
    for key, value in schema_dump.items():
        validate_before_set_value(key=key, value=value, data_base=data_base)
        if hasattr(ai, key):
            setattr(ai, key, value)
        else:
            set_value(ai, key, value, data_base=data_base)

    data_base.add(ai)
    data_base.commit()


def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIDetailPatch,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    update_ai_detail(data_base=data_base, token=token, schema=schema, ai_id=ai_id)
