from typing import Annotated

from fastapi import Depends, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from service.auth.router_logic.login import login

from database.database import database_dependency
from auth.jwt.issue_user_jwt import issue_user_jwt


def http_post(
    response: Response,
    data_base: database_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return login(response=response, data_base=data_base, form_data=form_data)
