from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models import User

from database.database import database_dependency
from execption_message.http_execption_params import http_exception_params
from auth.jwt.password_context import get_password_context


def validate_before_issue_user_jwt(
    data_base: database_dependency,
    form_data: OAuth2PasswordRequestForm,
    user: User,
):
    if not user:
        raise HTTPException(**http_exception_params["not_exist_user"])

    if user.is_banned:
        raise HTTPException(**http_exception_params["banned_user"])

    if not get_password_context().verify(
        (form_data.password + user.password_salt), user.password
    ):
        raise HTTPException(**http_exception_params["not_verified_password"])
