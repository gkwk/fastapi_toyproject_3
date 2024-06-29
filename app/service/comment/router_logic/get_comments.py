from database.database import database_dependency
from service.comment.logic_get_comments import logic_get_comments


def get_comments(data_base: database_dependency, post_id: int):
    filter_dict = {"post_id": post_id}

    return logic_get_comments(data_base=data_base, filter_dict=filter_dict)
