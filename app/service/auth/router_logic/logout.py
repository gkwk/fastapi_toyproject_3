from fastapi import Response, HTTPException
from sqlalchemy.exc import OperationalError


from database.database import database_dependency
from models import JWTList
from auth.jwt.refresh_token.delete_refresh_token import delete_refresh_token
from auth.jwt.access_token.ban_access_token import ban_access_token
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def logout(
    response: Response,
    data_base: database_dependency,
    access_token: current_user_access_token_payload,
):
    try:
        user_id = access_token.get("user_id")

        jwt = (
            data_base.query(JWTList)
            .filter_by(user_id=user_id)
            .limit(1)
            .with_for_update(nowait=True)
            .first()
        )

        response.delete_cookie(key="refresh_token")

        if jwt:
            ban_access_token(
                data_base=data_base,
                jwt=jwt,
            )
            delete_refresh_token(data_base=data_base, jwt=jwt)

        data_base.commit()
    except OperationalError as e:
        raise HTTPException(status_code=400)
