from typing import cast
import uuid

from fastapi import HTTPException, UploadFile, Depends, Path
from sqlalchemy import select


from database.database import database_dependency
from models import ChatSession
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.request_chat_session_detail_patch import (
    RequestChatSessionDetailPatch,
)
from exception_message.http_exception_params import http_exception_params


def validate_before_set_value(key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.
    pass


def set_value(
    chat_session: ChatSession, key: str, value, data_base: database_dependency
):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.
    pass


def update_chat_session_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionDetailPatch,
    chat_session_id: int,
):
    chat_session = data_base.query(ChatSession).filter_by(id=chat_session_id).first()

    if not chat_session:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    if token.get("user_id") != chat_session.user_create_id:
        raise HTTPException(**http_exception_params["not_verified_token"])

    # key가 없는 속성값은 제거한다. 이를 통해 None을 NULL값으로 사용할 수 있게된다.
    schema_dump = schema.model_dump(exclude_unset=True)

    # validation 함수와 setattr을 이용하여 속성값 변경 코드를 간단하게 표현하였다.
    # hasattr를 사용하여 속성이 없다면 개별적인 과정을 사용한다.
    for key, value in schema_dump.items():
        validate_before_set_value(key=key, value=value, data_base=data_base)
        if hasattr(chat_session, key):
            setattr(chat_session, key, value)
        else:
            set_value(chat_session, key, value, data_base=data_base)

    data_base.add(chat_session)
    data_base.commit()


def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestChatSessionDetailPatch,
    chat_session_id: int = Path(ge=1),
):
    """
    채팅 세션 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    update_chat_session_detail(
        data_base=data_base, token=token, schema=schema, chat_session_id=chat_session_id
    )
