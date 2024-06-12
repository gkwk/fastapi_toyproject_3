from fastapi import Path

from database.database import database_dependency
from models import AIlog
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def get_ailogs(
    data_base: database_dependency, token: current_user_access_token_payload, ai_id: int
):
    fileter_kwargs = {"ai_id": ai_id}

    if token.get("role") != "ROLE_ADMIN":
        fileter_kwargs["user_id"] = token.get("user_id")

    # token의 role을 이용하여 fastapi에서 자동으로 role에 맞는 값을 반환하도록 만든다.
    return {
        "role": token.get("role"),
        "ailogs": data_base.query(AIlog).filter_by(**fileter_kwargs).all(),
    }


def http_get(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    ai_id: int = Path(ge=1),
):
    """
    AI 모델 사용 로그 목록을 조회한다.
    """
    return get_ailogs(data_base=data_base, token=token, ai_id=ai_id)
