from fastapi import Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.ailog.router_logic.get_ailogs import get_ailogs


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델 사용 로그 목록을 조회한다.
    """
    return {
        "role": token.role,
        "ailogs": get_ailogs(
            data_base=data_base,
            user_id=token.user_id,
            user_role=token.role,
            ai_id=ai_id,
        ),
    }
