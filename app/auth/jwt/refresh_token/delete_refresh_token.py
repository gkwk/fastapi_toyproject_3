from fastapi import HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import StaleDataError


from models import JWTList
from database.database import database_dependency
from auth.jwt.access_token.ban_access_token import ban_access_token


def get_jwt(data_base: database_dependency, user_id: int):
    try:
        jwt = (
            data_base.query(JWTList)
            .filter_by(user_id=user_id)
            .limit(1)
            .with_for_update(nowait=True)
            .first()
        )
    except OperationalError as e:
        raise HTTPException(status_code=400)

    return jwt


def delete_refresh_token(
    data_base: database_dependency,
    jwt: JWTList | None,
):
    # access token ban은 사전에 수행되었다고 가정한다.
    if jwt is not None:
        data_base.delete(jwt)
