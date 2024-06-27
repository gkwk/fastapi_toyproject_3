from database.database import database_dependency
from service.chat.logic_get_chats import logic_get_chats


def get_chats(
    data_base: database_dependency,
    chat_session_id: int,
    user_id: int,
    user_role: str,
):
    filter_dict = {"chat_session_id": chat_session_id}

    if user_role != "ROLE_ADMIN":
        filter_dict["user_id"] = user_id

    return logic_get_chats(data_base=data_base, filter_dict=filter_dict)
