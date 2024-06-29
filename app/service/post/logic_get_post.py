from database.database import database_dependency
from models import Post


def logic_get_post(
    data_base: database_dependency,
    filter_dict: dict = {},
    order_dict: dict = {},
    with_for_update: bool = False,
    with_for_update_dict: dict = {},
):
    if with_for_update:
        return (
            data_base.query(Post)
            .filter_by(**filter_dict)
            .order_by(**order_dict)
            .limit(1)
            .with_for_update(**with_for_update_dict)
            .first()
        )

    return (
        data_base.query(Post)
        .filter_by(**filter_dict)
        .order_by(**order_dict)
        .limit(1)
        .first()
    )
