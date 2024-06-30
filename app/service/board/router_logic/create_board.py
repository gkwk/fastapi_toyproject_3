from fastapi import HTTPException
from sqlalchemy import select, insert, or_
from sqlalchemy.exc import IntegrityError

from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from database.cache import board_cache_set
from exception_message.sql_exception_messages import integrity_exception_messages
from models import User, JWTList, Board, UserPermissionTable, JWTAccessTokenBlackList
from auth.jwt.access_token.ban_access_token import ban_access_token


def user_board_permission_init(
    data_base: database_dependency,
    board: Board,
    is_visible: bool,
    user_id_list: list[int] = None,
):
    if not is_visible:
        new_permission_user_ids = set()

        if user_id_list:
            get_stmt = select(User.id).where(
                or_(User.id.in_(user_id_list), (User.role == "ROLE_ADMIN"))
            )

            new_permission_user_ids = set(
                data_base.execute(statement=get_stmt).scalars().all()
            )

            if new_permission_user_ids:
                insert_stmt = insert(UserPermissionTable).values(
                    [
                        {"board_id": board.id, "user_id": user_id}
                        for user_id in new_permission_user_ids
                    ]
                )

                data_base.execute(insert_stmt)

        else:
            get_stmt = select(User.id).where(User.role == "ROLE_ADMIN")

            new_permission_user_ids = set(
                data_base.execute(statement=get_stmt).scalars().all()
            )

            if new_permission_user_ids:
                insert_stmt = insert(UserPermissionTable).values(
                    [
                        {"board_id": board.id, "user_id": user_id}
                        for user_id in new_permission_user_ids
                    ]
                )

                data_base.execute(insert_stmt)

        for user_id in new_permission_user_ids:
            # 차후 timeout 등을 사용하는 법을 찾아본다.
            jwt = (
                data_base.query(JWTList)
                .filter_by(user_id=user_id)
                .limit(1)
                .with_for_update(nowait=True, skip_locked=True)
                .first()
            )

            if (
                (jwt is not None)
                and (jwt.access_token_uuid is not None)
                and (jwt.access_token_unix_timestamp is not None)
            ):
                blacklisted_access_token = (
                    data_base.query(JWTAccessTokenBlackList)
                    .filter_by(
                        user_id=user_id,
                        access_token_uuid=jwt.access_token_uuid,
                        access_token_unix_timestamp=jwt.access_token_unix_timestamp,
                    )
                    .limit(1)
                    .with_for_update(nowait=True, skip_locked=True)
                    .first()
                )
            else:
                blacklisted_access_token = None

            if jwt:
                ban_access_token(
                    data_base=data_base,
                    jwt=jwt,
                    blacklisted_access_token=blacklisted_access_token,
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

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()
        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    user_board_permission_init(
        data_base=data_base,
        board=board,
        is_visible=is_visible,
        user_id_list=user_id_list,
    )

    board.is_visible = is_visible
    board.is_available = is_available

    data_base.add(board)

    try:
        data_base.commit()
    except IntegrityError as e:
        data_base.rollback()
        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    board_cache_set(board_id=board.id, is_visible=is_visible)

    return board
