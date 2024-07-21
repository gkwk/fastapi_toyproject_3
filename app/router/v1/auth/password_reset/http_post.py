from fastapi import HTTPException, BackgroundTasks

from database.database import database_dependency
from schema.password_reset.request_password_reset_request import (
    RequestPasswordResetRequest,
)
from service.auth.router_logic.password_reset_request import (
    password_reset_request,
)


def http_post(
    data_base: database_dependency,
    background_tasks: BackgroundTasks,
    schema: RequestPasswordResetRequest,
):
    try:
        result_uuid = password_reset_request(
            data_base=data_base,
            background_tasks=background_tasks,
            user_email=schema.email,
        )

    except HTTPException as e:
        raise e

    return {"result": "success", "id": result_uuid}
