from typing import Annotated

from fastapi import Depends, Request, WebSocket
from fastapi.security import OAuth2PasswordBearer

from config.config import get_settings

# ref : https://github.com/tiangolo/fastapi/issues/2031
class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)

oauth2_scheme_v1 = OAuth2PasswordBearer(
    tokenUrl=get_settings().OAUTH_TOKEN_URL, scheme_name="v1_oauth2_schema"
)

oauth2_scheme_v1_test = CustomOAuth2PasswordBearer(
    tokenUrl=get_settings().OAUTH_TOKEN_URL, scheme_name="v1_oauth2_schema"
)

def get_oauth2_scheme_v1():
    # return oauth2_scheme_v1
    return oauth2_scheme_v1_test

jwt_dependency = Annotated[str, Depends(get_oauth2_scheme_v1())]
