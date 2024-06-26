from database.database import database_dependency
from models import AIlog


def logic_create_ailog(
    data_base: database_dependency,
    user_id: int,
    ai_id: int,
    description: str,
    result: str,
    celery_task_id: str,
):
    ailog = AIlog(
        user_id=user_id,
        ai_id=ai_id,
        description=description,
        result=result,
        celery_task_id=celery_task_id,
    )

    return ailog
