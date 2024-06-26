from database.database import database_dependency
from service.ailog.logic_get_ailogs import logic_get_ailogs


def get_ailogs(
    data_base: database_dependency, user_id: int, user_role: str, ai_id: int
):
    filter_dict = {"ai_id": ai_id}

    if user_role != "ROLE_ADMIN":
        filter_dict["user_id"] = user_id

    logic_get_ailogs(data_base=data_base, filter_dict=filter_dict)

    return logic_get_ailogs(data_base=data_base, filter_dict=filter_dict)
