from fastapi import HTTPException, Path

from database.database import database_dependency
from models import AI, AIlog
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message.http_exception_params import http_exception_params


def delete_ailog(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int,
    ailog_id: int,
):
    ai = data_base.query(AI).filter_by(id=ai_id).first()
    ailog = data_base.query(AIlog).filter_by(id=ailog_id, ai_id=ai_id).first()

    if (ai is None) or (ailog is None):
        raise HTTPException(**http_exception_params["not_exist_resource"])

    data_base.delete(ai)
    data_base.commit()



def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
    ailog_id: int = Path(ge=1),
):
    """
    AI 모델의 로그를 삭제한다.
    """
    delete_ailog(data_base=data_base, token=token, ai_id=ai_id, ailog_id=ailog_id)
