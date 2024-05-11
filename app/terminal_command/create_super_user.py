import secrets
import getpass

from sqlalchemy.orm import Session

from models import User
from schema.terminal import AdminCreateEmail, AdminCreateName, AdminCreatePassword
from database.database import database_dependency, get_data_base_decorator
from auth.jwt.password_context import get_password_context
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


def validate_admin_name(data_base: Session, debug: bool):
    while True:
        try:
            name = input("Admin name : ")
            if get_user_with_username(data_base=data_base, name=name):
                raise ValueError(
                    http_exception_params["not_unique_user_name"]["detail"]
                )
            AdminCreateName(name=name)
            break
        except Exception as ex:
            print(ex)

            if debug:
                raise ValueError()

    return name


def validate_admin_email(data_base: Session, debug: bool):
    while True:
        try:
            email = input("Admin email : ")
            if get_user_with_email(data_base=data_base, eamil=email):
                raise ValueError(http_exception_params["not_unique_email"]["detail"])
            AdminCreateEmail(email=email)
            break
        except Exception as ex:
            print(ex)

            if debug:
                raise ValueError()

    return email


def validate_admin_password(data_base: Session, debug: bool):
    while True:
        try:
            password1 = getpass.getpass("Password : ")
            password2 = getpass.getpass("Password Confirm : ")
            AdminCreatePassword(password1=password1, password2=password2)
            break
        except Exception as ex:
            print(ex)
            if debug:
                raise ValueError()

    return password1


def database_process(
    data_base: Session,
    name: str,
    password1: str,
    generated_password_salt: str,
    email: str,
):
    user = User(
        name=name,
        password=get_password_context().hash(password1 + generated_password_salt),
        password_salt=generated_password_salt,
        email=email,
        role="ROLE_ADMIN",
    )
    data_base.add(user)
    data_base.commit()
    
    return user


@get_data_base_decorator
def create_admin_with_terminal(data_base: Session = None, debug=False):
    generated_password_salt = secrets.token_hex(4)

    name = validate_admin_name(data_base=data_base, debug=debug)
    email = validate_admin_email(data_base=data_base, debug=debug)
    password1 = validate_admin_password(data_base=data_base, debug=debug)

    user = database_process(
        data_base=data_base,
        name=name,
        password1=password1,
        generated_password_salt=generated_password_salt,
        email=email,
    )

    if debug:
        return user.id
