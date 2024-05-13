from starlette import status

from router.v1 import v1_url
from router.v1.boards.router import router
from database.database import database_dependency
from models import User, JWTList, Board
from auth.jwt.access_token.ban_access_token import ban_access_token
from schema.boards.request_board_create import RequestBoardCreate

def user_board_permission_init(
    data_base: database_dependency,
    board: Board,
    is_visible: bool,
    user_id_list: list[int] = None,
):
    users = []
    board.permission_verified_user_id_range = (
        data_base.query(User).order_by(User.id.desc()).first().id
    )

    if is_visible:
        if user_id_list:
            users = (
                data_base.query(User)
                .filter(User.id.in_(user_id_list))
                .order_by(User.id.asc())
                .all()
            )

        else:
            users = data_base.query(User).order_by(User.id.asc()).all()

    else:
        if user_id_list:
            users = (
                data_base.query(User)
                .filter(User.id.in_(user_id_list))
                .order_by(User.id.asc())
                .all()
            )

        else:
            users = (
                data_base.query(User)
                .filter_by(role="ROLE_ADMIN")
                .order_by(User.id.asc())
                .all()
            )

    if users:
        for user in users:
            user.boards.append(board)

    data_base.commit()

    users_refresh_token_table = (
        data_base.query(JWTList)
        .filter(JWTList.user_id <= board.permission_verified_user_id_range)
        .all()
    )

    for user in users_refresh_token_table:
        ban_access_token(
            data_base=data_base,
            user_id=user.user_id,
        )


def create_board(
    data_base: database_dependency,
    name: str,
    information: str,
    is_visible: bool,
    is_available: bool,
    user_id_list: list[int] = None,
):
    board = Board(name=name, information=information)
    data_base.add(board)
    data_base.commit()
    
    user_board_permission_init(data_base=data_base, board=board, is_visible=is_visible, user_id_list=user_id_list)

    board.is_visible = is_visible
    board.is_available = is_available
    data_base.add(board)
    data_base.commit()

    return board.id


@router.post(v1_url.BOARDS_ROOT, status_code=status.HTTP_201_CREATED)
def http_post(data_base: database_dependency, schema: RequestBoardCreate):
    """
    게시판을 생성한다.
    """

    board_id = create_board(
        data_base=data_base,
        name=schema.name,
        information=schema.information,
        is_visible=schema.is_visible,
        is_available=schema.is_available,
        user_id_list=schema.user_id_list,
    )

    return {"result": "success", "id": board_id}
