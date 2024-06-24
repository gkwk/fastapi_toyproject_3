from fastapi import HTTPException

from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from schema.users.request_user_detail_patch import RequestUserDetailPatch
from service.user.router_logic.update_user import update_user


def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestUserDetailPatch,
    user_id: int,
):
    """
    사용자 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    try:
        update_user(data_base=data_base, token=token, schema=schema, user_id=user_id)
    except HTTPException as e:
        raise e
