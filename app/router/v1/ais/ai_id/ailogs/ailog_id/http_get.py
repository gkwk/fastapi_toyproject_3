from fastapi import Path, HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.ailog.router_logic.get_ailog_detail import get_ailog_detail


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
    ailog_id: int = Path(ge=1),
):
    """
    AI 모델의 로그 상세 정보를 조회한다.
    """
    # scope 등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드로의 변경을 차후 고려해본다.

    try:
        ailog = get_ailog_detail(
            data_base=data_base,
            ai_id=ai_id,
            ailog_id=ailog_id,
            user_id=token.user_id,
            user_role=token.role,
        )
    except HTTPException as e:
        raise e

    return {"role": token.role, "detail": ailog}
