from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from celery.result import AsyncResult


from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message.sql_exception_messages import integrity_exception_messages

from schema.ais.request_ai_create import RequestAICreate
from celery_app.celery import celery_app
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

    async_task: AsyncResult = celery_app.send_task(
        name="train_ai_task",
        kwargs={
            "ai_id": ai.id,
            "ai_name": ai.name,
            "ai_type": ai.ai_type,
            "is_visible": schema.is_visible,
        },
        task_id=celery_task_id,
    )

    return (async_task, ai)
