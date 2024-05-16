import json

from fastapi import HTTPException, Path
from celery import uuid
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.ais.ai_id.ailogs.router import router
from database.database import database_dependency
from models import User, JWTList, Board, AI, AIlog
from auth.jwt.access_token.ban_access_token import ban_access_token
from schema.ailogs.request_ailog_create import RequestAIlogCreate
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from execption_message.http_execption_params import http_exception_params
from celery_app.v1.ailogs.tasks import celery_task_ai_infer

json_encoder = json.JSONEncoder()
json_decoder = json.JSONDecoder()


def create_ailog(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIlogCreate,
    ai_id: int,
):
    celery_task_id = uuid()
    ai = data_base.query(AI).filter_by(id=ai_id).first()

    if (not ai) or (not ai.is_available) or (not ai.is_visible):
        raise HTTPException(**http_exception_params["not_exist_ai_model"])

    ailog = AIlog(
        user_id=token.get("user_id"),
        ai_id=ai_id,
        description=schema.description,
        result=json_encoder.encode({"result": None}),
        celery_task_id=celery_task_id,
    )

    data_base.add(ailog)
    data_base.commit()

    async_task = celery_task_ai_infer.apply_async(
        kwargs={"data_base": None, "ai_id": ai.id, "ailog_id": ailog.id},
        task_id=celery_task_id,
    )
    return (async_task, ailog.id)


@router.post(
    v1_url.ENDPOINT, status_code=status.HTTP_202_ACCEPTED, tags=[v1_tags.AILOG_TAG]
)
def http_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIlogCreate,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델 사용 로그를 생성한다.
    """

    async_task, ai_id = create_ailog(data_base=data_base, token=token, schema=schema, ai_id=ai_id)

    return {"task_id": async_task.id, "id": ai_id}
