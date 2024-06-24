from database.database import database_dependency
from service.user.logic_get_users import logic_get_users


def get_users(
    data_base: database_dependency, filter_dict: dict = {}, order_dict: dict = {}
):
    return logic_get_users(
        data_base=data_base, filter_dict=filter_dict, order_dict=order_dict
    )
