from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.ailogs.request_ailog_detail_patch import RequestAIlogDetailPatch
from service.ailog.router_logic.update_ailog import update_ailog_detail


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
    try:
        update_ailog_detail(
            data_base=data_base,
            token=token,
            schema=schema,
            ai_id=ai_id,
            ailog_id=ailog_id,
        )
    except HTTPException as e:
        raise e
