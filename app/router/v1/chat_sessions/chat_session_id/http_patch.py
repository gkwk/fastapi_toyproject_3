from fastapi import HTTPException, Path

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.chat_sessions.request_chat_session_detail_patch import (
    RequestChatSessionDetailPatch,
)
from service.chat_session.router_logic.update_chat_session import (
    update_chat_session_detail,
)


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
    try:
        update_chat_session_detail(
            data_base=data_base,
            token=token,
            schema=schema,
            chat_session_id=chat_session_id,
        )
    except HTTPException as e:
        raise e
