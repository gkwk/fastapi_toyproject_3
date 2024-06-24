from database.database import database_dependency
from service.user.logic_get_user import logic_get_user


def logic_get_user_with_email(
    data_base: database_dependency,
    email: str,
    with_for_update: bool = False,
    with_for_update_dict: dict = {},
):
    return logic_get_user(
        data_base=data_base,
        filter_dict={"email": email},
        with_for_update=with_for_update,
        with_for_update_dict=with_for_update_dict,
    )
