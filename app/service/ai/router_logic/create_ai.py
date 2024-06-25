from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message import http_exception_params
from exception_message.sql_exception_messages import integrity_exception_messages

from schema.ais.request_ai_create import RequestAICreate
from celery_app.v1.ais.tasks import celery_task_ai_train
from service.ai.logic_create_ai import logic_create_ai


def create_ai(data_base: database_dependency, schema: RequestAICreate):
    ai, celery_task_id = logic_create_ai(data_base=data_base, schema=schema)

    data_base.add(ai)

    try:
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    async_task = celery_task_ai_train.apply_async(
        kwargs={"data_base": None, "ai_id": ai.id, "is_visible": schema.is_visible},
        task_id=celery_task_id,
    )

    return (async_task, ai)
