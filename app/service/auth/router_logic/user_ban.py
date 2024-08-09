from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from models import User, JWTList
from database.database import database_dependency
from custom_exception.custom_exception import (
    BannedUserHTTPException,
    NotExistUserHTTPException,
)
from exception_message import http_exception_params
from auth.jwt.access_token.ban_access_token import ban_access_token
from auth.jwt.refresh_token.delete_refresh_token import delete_refresh_token
from service.user.logic_get_user_with_id import logic_get_user_with_id


def _validate_user(data_base: database_dependency, user: User | None):
    if not user:
        raise NotExistUserHTTPException(**http_exception_params.not_exist_user)


def user_ban(data_base: database_dependency, user_id: int, ban: bool):
    try:
        user = logic_get_user_with_id(
            data_base,
            user_id,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )

        _validate_user(data_base=data_base, user=user)

        if ban:
            user.is_banned = True

            jwt = (
                data_base.query(JWTList)
                .filter_by(user_id=user.id)
                .limit(1)
                .with_for_update(nowait=True)
                .first()
            )

            ban_access_token(
                data_base=data_base,
                jwt=jwt,
            )

            delete_refresh_token(data_base=data_base, jwt=jwt)

        else:
            user.is_banned = False

        data_base.commit()

    except OperationalError as e:
        raise HTTPException(status_code=400)
