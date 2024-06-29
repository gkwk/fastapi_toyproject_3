from fastapi import HTTPException

from database.database import database_dependency
from exception_message import http_exception_params
from service.post.logic_get_post import logic_get_post


def get_post_detail(
    data_base: database_dependency,
    board_id: int,
    post_id: int,
    user_role: str,
):
    filter_dict = {"id": post_id, "board_id": board_id}

    if user_role != "ROLE_ADMIN":
        filter_dict["is_visible"] = True

    post = logic_get_post(data_base=data_base, filter_dict=filter_dict)

    if post is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    return post
