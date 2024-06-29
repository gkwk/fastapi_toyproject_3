from database.database import database_dependency
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from models import Comment


def logic_create_comment(
    data_base: database_dependency,
    token: current_user_access_token_payload,
    post_id: int,
    content: str,
    is_visible: bool,
    is_file_attached: bool,
):
    comment = Comment(
        user_id=token.user_id,
        post_id=post_id,
        content=content,
        is_visible=is_visible,
        is_file_attached=is_file_attached,
    )

    return comment
