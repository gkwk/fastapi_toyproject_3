from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from models import JWTList
from database.database import database_dependency


def delete_refresh_token(
    data_base: database_dependency,
    jwt: JWTList | None,
):
    # access token ban은 사전에 수행되었다고 가정한다.
    if jwt is not None:
        data_base.delete(jwt)
