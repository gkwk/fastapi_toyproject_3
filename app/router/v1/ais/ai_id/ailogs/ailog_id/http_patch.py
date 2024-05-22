from typing import cast
import uuid

from fastapi import HTTPException, UploadFile, Depends, Path
from starlette import status
from sqlalchemy import select

from router.v1 import v1_url, v1_tags
from router.v1.ais.ai_id.ailogs.ailog_id.router import router
from database.database import database_dependency
from models import AI, AIlog
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.ailogs.request_ailog_detail_patch import RequestAIlogDetailPatch
from exception_message.http_exception_params import http_exception_params


def validate_before_set_value(key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.
    pass


def set_value(ai: AI, key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.
    pass


def update_ai_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIlogDetailPatch,
    ai_id: int,
    ailog_id: int,
):
    ai = data_base.query(AI).filter_by(id=ai_id).first()
    ailog = data_base.query(AIlog).filter_by(id=ailog_id, ai_id=ai_id).first()

    if (ai is None) or (ailog is None):
        raise HTTPException(**http_exception_params["not_exist_resource"])

    if token.get("user_id") != ailog.user_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    # key가 없는 속성값은 제거한다. 이를 통해 None을 NULL값으로 사용할 수 있게된다.
    schema_dump = schema.model_dump(exclude_unset=True)

    # validation 함수와 setattr을 이용하여 속성값 변경 코드를 간단하게 표현하였다.
    # hasattr를 사용하여 속성이 없다면 개별적인 과정을 사용한다.
    # is_visible, is_available이 수정되면 사용자 접근 권한을 초기화하고, permission_verified_user_id_range을 0으로 바꾸는 함수를 차후 추가한다.
    for key, value in schema_dump.items():
        validate_before_set_value(key=key, value=value, data_base=data_base)
        if hasattr(ailog, key):
            setattr(ailog, key, value)
        else:
            set_value(ailog, key, value, data_base=data_base)

    data_base.add(ailog)
    data_base.commit()


@router.patch(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.AILOG_TAG]
)
def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIlogDetailPatch,
    ai_id: int = Path(ge=1),
    ailog_id: int = Path(ge=1),
):
    """
    AI 모델의 로그 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    update_ai_detail(
        data_base=data_base, token=token, schema=schema, ai_id=ai_id, ailog_id=ailog_id
    )
