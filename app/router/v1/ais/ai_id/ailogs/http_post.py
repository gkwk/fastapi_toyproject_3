from fastapi import Path

from database.database import database_dependency
from schema.ailogs.request_ailog_create import RequestAIlogCreate
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from service.ailog.router_logic.create_ailog import create_ailog


def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIlogCreate,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델 사용 로그를 생성한다.
    """
    async_task, ailog = create_ailog(
        data_base=data_base, token=token, schema=schema, ai_id=ai_id
    )

    return {"task_id": async_task.id, "id": ailog.id}
