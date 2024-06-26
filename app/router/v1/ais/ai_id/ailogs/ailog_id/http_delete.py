from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.ailog.router_logic.delete_ailog import delete_ailog


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
    ailog_id: int = Path(ge=1),
):
    """
    AI 모델의 로그를 삭제한다.
    """
    try:
        delete_ailog(data_base=data_base, token=token, ai_id=ai_id, ailog_id=ailog_id)
    except HTTPException as e:
        raise e
