from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.ais.request_ai_detail_patch import RequestAIDetailPatch
from service.ai.router_logic.update_ai import update_ai_detail


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
    try:
        update_ai_detail(data_base=data_base, schema=schema, ai_id=ai_id)
    except HTTPException as e:
        raise e
