from typing import Union

from fastapi import Path, HTTPException

from router.v1 import v1_url, v1_tags
from router.v1.ais.ai_id.router import router
from database.database import database_dependency
from models import AI
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.ais.response_ai_detail import (
    ResponseAIDetailForUser,
    ResponseAIDetailForAdmin,
)
from exception_message.http_exception_params import http_exception_params


def get_ai_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int,
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.

    ai = data_base.query(AI).filter_by(id=ai_id).first()

    if not ai:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    return {
        "role": token.get("role"),
        "detail": ai,
    }


@router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseAIDetailForUser, ResponseAIDetailForAdmin],
    tags=[v1_tags.AI_TAG],
)
def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델 상세 정보를 조회한다.
    """
    return get_ai_detail(data_base=data_base, token=token, ai_id=ai_id)
