from database.database import database_dependency
from service.post.logic_get_posts import logic_get_posts


def get_posts(data_base: database_dependency, board_id: int, user_role: str):
    filter_dict = {"board_id": board_id}

    if user_role != "ROLE_ADMIN":
        filter_dict["is_visible"] = True

    return logic_get_posts(data_base=data_base, filter_dict=filter_dict)
