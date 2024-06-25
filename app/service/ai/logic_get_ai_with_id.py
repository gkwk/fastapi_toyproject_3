from database.database import database_dependency
from service.ai.logic_get_ai import logic_get_ai


def logic_get_ai_with_id(
    data_base: database_dependency,
    ai_id: int,
    with_for_update: bool = False,
    with_for_update_dict: dict = {},
):
    return logic_get_ai(
        data_base=data_base,
        filter_dict={"id": ai_id},
        with_for_update=with_for_update,
        with_for_update_dict=with_for_update_dict,
    )
