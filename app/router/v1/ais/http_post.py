from celery import uuid

from database.database import database_dependency
from models import User, JWTList, Board, AI
from auth.jwt.access_token.ban_access_token import ban_access_token
from schema.ais.request_ai_create import RequestAICreate
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from celery_app.v1.ais.tasks import celery_task_ai_train


def create_ai(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAICreate,
):
    celery_task_id = uuid()
    ai = AI(
        name=schema.name,
        description=schema.description,
        is_visible=False,
        celery_task_id=celery_task_id,
    )
    data_base.add(ai)
    data_base.commit()

    async_task = celery_task_ai_train.apply_async(
        kwargs={"data_base": None, "ai_id": ai.id, "is_visible": schema.is_visible},
        task_id=celery_task_id,
    )
    return (async_task, ai.id)


def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAICreate,
):
    """
    AI 모델을 생성한다.
    """

    async_task, ai_id = create_ai(data_base=data_base, token=token, schema=schema)

    return {"task_id": async_task.id, "id": ai_id}
