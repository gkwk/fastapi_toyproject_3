import secrets

from fastapi import HTTPException
from starlette import status
from sqlalchemy import select

from router.v1 import v1_url, v1_tags
from router.v1.boards.id.router import router
from database.database import database_dependency
from models import Board, UserPermissionTable, User
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from auth.jwt.password_context import get_password_context
from schema.boards.request_board_detail_patch import RequestBoardDetailPatch
from execption_message.http_execption_params import http_exception_params


def get_board_with_name(data_base: database_dependency, name: str):
    return data_base.query(Board).filter_by(name=name).first()


def validate_before_set_value(key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.

    if key == "name":
        if get_board_with_name(data_base=data_base, name=value):
            raise HTTPException(**http_exception_params["not_unique_attribute_value"])


def set_value(board: Board, key: str, value, data_base: database_dependency):
    # dict 등을 이용하여 if문을 사용하지 않는 방향으로 코드를 개선한다.

    if key == "user_list_permission_append":
        # SQLAlchemy 2.0 방식을 사용한다.
        stmt = select(UserPermissionTable.user_id).where(
            UserPermissionTable.board_id == board.id
        )

        already_has_permission_user_id_set = set(
            data_base.execute(statement=stmt).scalars().all()
        )

        not_has_permission_user_id_set = set(value) - already_has_permission_user_id_set

        stmt = select(User).where(User.id.in_(not_has_permission_user_id_set))

        users = data_base.execute(statement=stmt).scalars().all()
        board.users.append(*users)

    elif key == "user_list_permission_remove":
        stmt = select(UserPermissionTable.user_id).where(
            UserPermissionTable.board_id == board.id
        )
        already_has_permission_user_id_set = set(
            data_base.execute(statement=stmt).scalars().all()
        )

        has_permission_user_id_set = set(value) & already_has_permission_user_id_set

        stmt = select(User).where(User.id.in_(has_permission_user_id_set))

        users = data_base.execute(statement=stmt).scalars().all()
        board.users.remove(*users)


def update_board_detail(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestBoardDetailPatch,
    board_id: int,
):
    board = data_base.query(Board).filter_by(id=board_id).first()

    if not board:
        raise HTTPException(**http_exception_params["not_exist_resource"])

    # key가 없는 속성값은 제거한다. 이를 통해 None을 NULL값으로 사용할 수 있게된다.
    schema_dump = schema.model_dump(exclude_unset=True)

    # validation 함수와 setattr을 이용하여 속성값 변경 코드를 간단하게 표현하였다.
    # hasattr를 사용하여 속성이 없다면 개별적인 과정을 사용한다.
    # is_visible, is_available이 수정되면 사용자 접근 권한을 초기화하고, permission_verified_user_id_range을 0으로 바꾸는 함수를 차후 추가한다.
    for key, value in schema_dump.items():
        validate_before_set_value(key=key, value=value, data_base=data_base)
        if hasattr(board, key):
            setattr(board, key, value)
        else:
            set_value(board, key, value, data_base=data_base)

    data_base.add(board)
    data_base.commit()


@router.patch(v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.BOARD_TAG])
def http_patch(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    schema: RequestBoardDetailPatch,
    board_id: int,
):
    """
    게시판 상세 정보를 수정한다.
    """
    # 차후 권한에 따라 수정 가능한 필드를 제한하는 기능을 추가한다.
    update_board_detail(data_base=data_base, token=token, schema=schema, board_id=board_id)
