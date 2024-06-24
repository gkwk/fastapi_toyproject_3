from fastapi import Response, HTTPException
from sqlalchemy.exc import OperationalError


from database.database import database_dependency
from models import JWTList, JWTAccessTokenBlackList
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
                .with_for_update(nowait=True)
                .first()
            )
        else:
            blacklisted_access_token = None

        response.delete_cookie(key="refresh_token")

        if jwt:
            ban_access_token(
                data_base=data_base,
                jwt=jwt,
                blacklisted_access_token=blacklisted_access_token,
            )
            delete_refresh_token(data_base=data_base, jwt=jwt)

        data_base.commit()
    except OperationalError as e:
        raise HTTPException(status_code=400)
