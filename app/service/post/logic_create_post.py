from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from models import Post


def logic_create_post(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    board_id: int,
    name: str,
    content: str,
    is_visible: bool,
    is_file_attached: bool,
):
    post = Post(
        user_id=token.user_id,
        board_id=board_id,
        name=name,
        content=content,
        is_visible=is_visible,
        is_file_attached=is_file_attached,
    )

    return post
