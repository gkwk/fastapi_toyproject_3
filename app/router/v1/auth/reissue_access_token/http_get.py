from typing import Annotated

from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from router.v1 import v1_url, v1_tags
from router.v1.auth.reissue_access_token.router import router
from database.database import database_dependency
from auth.jwt.reissue_access_token import reissue_access_token
from auth.jwt.refresh_token.get_user_refresh_token_payload import current_user_refresh_token_payload


@router.get(v1_url.ENDPOINT, tags=[v1_tags.AUTH_TAG])
def http_get(
    data_base: database_dependency,
    token : current_user_refresh_token_payload
):
    tokens = reissue_access_token(data_base=data_base, refresh_token_payload=token)
    
    return {
        "access_token": tokens.get("access_token"),
        "token_type": tokens.get("token_type"),
    }
