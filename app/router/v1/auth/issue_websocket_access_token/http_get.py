from typing import Annotated

from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from router.v1 import v1_url, v1_tags
from router.v1.auth.issue_websocket_access_token.router import router
from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from auth.jwt.websocket_access_token.generate_websocket_access_token import (
    generate_websocket_access_token,
)


@router.get(v1_url.ENDPOINT, tags=[v1_tags.AUTH_TAG])
def http_get(data_base: database_dependency, token: current_user_access_token_payload):
    wensocket_access_token = generate_websocket_access_token(
        data_base=data_base, user_id=token.get("user_id"), user_role=token.get("role")
    )

    return {
        "websocket_access_token": wensocket_access_token,
        "token_type": "bearer",
    }
