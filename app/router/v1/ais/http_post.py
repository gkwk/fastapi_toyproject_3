from fastapi import HTTPException

from database.database import database_dependency
from schema.ais.request_ai_create import RequestAICreate
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.ai.router_logic.create_ai import create_ai


def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAICreate,
):
    """
    AI 모델을 생성한다.
    """
    try:
        async_task, ai = create_ai(data_base=data_base, schema=schema)
    except HTTPException as e:
        raise e

    return {"task_id": async_task.id, "id": ai.id}
