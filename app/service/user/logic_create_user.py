import secrets

from database.database import database_dependency
from models import User
from auth.jwt.password_context import get_password_context


def logic_create_user(
    data_base: database_dependency,
    name: str,
    password: str,
    email: str,
    commit: bool = True,
):
    generated_password_salt = secrets.token_hex(4)
    user = User(
        name=name,
        password=get_password_context().hash(password + generated_password_salt),
        password_salt=generated_password_salt,
        role="ROLE_USER",
        email=email,
    )
    data_base.add(user)

    if commit:
        data_base.commit()

    return user
