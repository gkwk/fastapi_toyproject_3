from celery import uuid

from database.database import database_dependency
from models import AI
from schema.ais.request_ai_create import RequestAICreate


def logic_create_ai(data_base: database_dependency, schema: RequestAICreate):
    celery_task_id = uuid()
    ai = AI(
        name=schema.name,
        description=schema.description,
        is_visible=False,
        ai_type=schema.ai_type,
        celery_task_id=celery_task_id,
    )

    return (ai, celery_task_id)
