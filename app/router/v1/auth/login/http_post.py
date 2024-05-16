from typing import Annotated

from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from router.v1 import v1_url, v1_tags
from router.v1.auth.login.router import router
from database.database import database_dependency
from auth.jwt.issue_user_jwt import issue_user_jwt


# @router.post(v1_url.LOGIN_ROOT, response_model=user_schema.ResponseUserToken)
@router.post(v1_url.ENDPOINT, tags=[v1_tags.AUTH_TAG])
def http_post(
    response: Response,
    data_base: database_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    tokens = issue_user_jwt(data_base=data_base, form_data=form_data)

    response.set_cookie(
        key="refresh_token",
        value=tokens.get("refresh_token"),
        httponly=True,
        max_age=24 * 60 * 60,  # 만료 시간 (단위 : second)
        path="/",
        samesite="lax",
        secure=False,  # HTTPS 환경에서만 쿠키 전송 허용 여부
    )

    return {
        "access_token": tokens.get("access_token"),
        "token_type": tokens.get("token_type"),
    }
