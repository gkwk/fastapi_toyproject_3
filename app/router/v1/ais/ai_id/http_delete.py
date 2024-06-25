from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.ai.router_logic.delete_ai import delete_ai


def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델을 삭제한다.
    """

    try:
        delete_ai(data_base=data_base, ai_id=ai_id)
    except HTTPException as e:
        raise e
