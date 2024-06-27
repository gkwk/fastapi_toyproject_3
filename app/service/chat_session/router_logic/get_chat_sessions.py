from database.database import database_dependency
from service.chat_session.logic_get_chat_sessions import logic_get_chat_sessions


def get_chat_sessions(
    data_base: database_dependency, filter_dict: dict = {}, order_dict: dict = {}
):
    return logic_get_chat_sessions(
        data_base=data_base, filter_dict=filter_dict, order_dict=order_dict
    )
