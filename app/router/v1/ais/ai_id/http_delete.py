from fastapi import HTTPException, Path
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.ais.ai_id.router import router
from database.database import database_dependency
from models import AI
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from exception_message.http_exception_params import http_exception_params


def delete_ai(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int,
):
    ai = data_base.query(AI).filter_by(id=ai_id).first()

    if ai is None:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    data_base.delete(ai)
    data_base.commit()


@router.delete(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.AI_TAG]
)
def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델을 삭제한다.
    """
    delete_ai(data_base=data_base, token=token, ai_id=ai_id)
