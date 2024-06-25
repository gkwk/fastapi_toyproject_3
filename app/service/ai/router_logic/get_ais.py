from database.database import database_dependency
from service.ai.logic_get_ais import logic_get_ais


def get_ais(
    data_base: database_dependency, filter_dict: dict = {}, order_dict: dict = {}
):
    return logic_get_ais(
        data_base=data_base, filter_dict=filter_dict, order_dict=order_dict
    )
