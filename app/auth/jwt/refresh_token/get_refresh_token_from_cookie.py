from typing import Annotated

from fastapi import Request, Depends


def get_refresh_token_from_cookie(request: Request):
    refresh_token = request.cookies.get("refresh_token", "")

    return refresh_token

refresh_token_dependency = Annotated[dict, Depends(get_refresh_token_from_cookie)]
