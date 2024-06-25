from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError


from database.database import database_dependency
from database.integrity_error_message_parser import intergrity_error_message_parser
from exception_message import http_exception_params, sql_exception_messages
from exception_message.sql_exception_messages import integrity_exception_messages
from service.ai.logic_get_ai_with_id import logic_get_ai_with_id


def delete_ai(data_base: database_dependency, ai_id: int):

    try:
        ai = logic_get_ai_with_id(
            data_base=data_base,
            ai_id=ai_id,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )
    except OperationalError as e:
        raise HTTPException(**sql_exception_messages.unknown_error)

    if ai is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    data_base.delete(ai)

    try:
        data_base.commit()
        # 파일 삭제 과정을 실행하는 코드를 작성한다.

    except IntegrityError as e:
        data_base.rollback()

        error_code = intergrity_error_message_parser.parsing(
            integrity_error_message_orig=e.orig
        )
        raise HTTPException(**integrity_exception_messages(error_code))
