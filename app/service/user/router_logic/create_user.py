from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError


from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message import http_exception_params
from exception_message.sql_exception_messages import integrity_exception_messages
from service.user.logic_get_user_with_email import logic_get_user_with_email
from service.user.logic_get_user_with_username import logic_get_user_with_username
from service.user.logic_create_user import logic_create_user


def create_user(data_base: database_dependency, name: str, password: str, email: str):
    user = logic_create_user(
        data_base=data_base, name=name, password=password, email=email, commit=False
    )
    data_base.add(user)

    try:
        data_base.commit()

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))

    return user
