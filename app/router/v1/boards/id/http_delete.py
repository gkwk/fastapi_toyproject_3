from fastapi import HTTPException
from starlette import status

from router.v1 import v1_url
from router.v1.boards.router import router
from database.database import database_dependency
from models import Board
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from execption_message.http_execption_params import http_exception_params


def delete_board(
    data_base: database_dependency, token: current_user_access_token_payload, id: int
):
    # 차후 scope 등으로 변경한다.
    if token.get("role") != "ROLE_ADMIN":
        raise HTTPException(**http_exception_params["not_verified_token"])

    board = data_base.query(Board).filter_by(id=id).first()

    data_base.delete(board)
    data_base.commit()


@router.delete(v1_url.BOARDS_ID, status_code=status.HTTP_204_NO_CONTENT)
def http_delete(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    id: int,
):
    """
    게시판을 삭제한다.
    """
    delete_board(data_base=data_base, token=token, id=id)
