import json

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from celery import uuid
from celery.result import AsyncResult


from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message import http_exception_params
from exception_message.sql_exception_messages import integrity_exception_messages
from schema.ailogs.request_ailog_create import RequestAIlogCreate
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from celery_app.celery import celery_app
from service.ailog.logic_create_ailog import logic_create_ailog
from service.ai.logic_get_ai_with_id import logic_get_ai_with_id

json_encoder = json.JSONEncoder()


def create_ailog(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestAIlogCreate,
    ai_id: int,
):
    celery_task_id = uuid()
    ai = logic_get_ai_with_id(data_base=data_base, ai_id=ai_id)

    # DB FK 제약으로 ai가 db에 없을 시 에러를 출력하지만, 사용 조건 검사를 위해 추가하였음.
    if (not ai) or (not ai.is_available) or (not ai.is_visible):
        raise HTTPException(**http_exception_params.not_exist_ai_model)

    ailog = logic_create_ailog(
        data_base=data_base,
        user_id=token.user_id,
        ai_id=ai_id,
        description=schema.description,
        result=json_encoder.encode({"result": None}),
        celery_task_id=celery_task_id,
    )

    data_base.add(ailog)

    try:
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    async_task: AsyncResult = celery_app.send_task(
        name="infer_ai_task",
        kwargs={
            "ai_id": ai.id,
            "ai_name": ai.name,
            "ai_type": ai.ai_type,
            "ailog_id": ailog.id,
        },
        task_id=celery_task_id,
    )
    return (async_task, ailog)
