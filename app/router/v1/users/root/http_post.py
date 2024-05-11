import secrets

from fastapi import HTTPException
from starlette import status

from router.v1 import v1_url
from router.v1.users.router import router
from database.database import database_dependency
from models import User
from auth.jwt.password_context import get_password_context
from app.schema.users.request_user_join import RequestUserJoin
from execption_message.http_execption_params import http_exception_params


def get_user_with_username(
    data_base: database_dependency,
    name: str,
):
    return data_base.query(User).filter_by(name=name).first()


def get_user_with_email(
    data_base: database_dependency,
    eamil: str,
):
    return data_base.query(User).filter_by(email=eamil).first()


def create_user(
    data_base: database_dependency,
    name: str,
    password: str,
    email: str,
):
    if get_user_with_username(data_base=data_base, name=name):
        raise HTTPException(**http_exception_params["not_unique_user_name"])
    if get_user_with_email(data_base=data_base, eamil=email):
        raise HTTPException(**http_exception_params["not_unique_email"])

    generated_password_salt = secrets.token_hex(4)
    user = User(
        name=name,
        password=get_password_context().hash(password + generated_password_salt),
        password_salt=generated_password_salt,
        role="ROLE_USER",
        email=email,
    )
    data_base.add(user)
    data_base.commit()

    return user.id


@router.post(v1_url.USERS_ROOT, status_code=status.HTTP_201_CREATED)
def http_post(data_base: database_dependency, schema: RequestUserJoin):
    user_id = create_user(
        data_base=data_base,
        name=schema.name,
        password=schema.password1,
        email=schema.email,
    )

    return {"result": "success", "id": user_id}
