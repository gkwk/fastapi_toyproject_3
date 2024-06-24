from database.database import database_dependency
from models import User


def logic_get_users(
    data_base: database_dependency,
    filter_dict: dict = {},
    order_dict: dict = {},
    with_for_update: bool = False,
    with_for_update_dict: dict = {},
):
    if with_for_update:
        return (
            data_base.query(User)
            .filter_by(**filter_dict)
            .order_by(**order_dict)
            .with_for_update(**with_for_update_dict)
            .all()
        )

    return data_base.query(User).filter_by(**filter_dict).order_by(**order_dict).all()
