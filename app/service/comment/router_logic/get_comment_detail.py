from fastapi import HTTPException

from database.database import database_dependency
from exception_message import http_exception_params
from service.comment.logic_get_comment import logic_get_comment


def get_comment_detail(
    data_base: database_dependency,
    post_id: int,
    comment_id: int,
):
    # scope등으로 접근 권한을 확인하여 정보의 반환 여부를 제어하도록 하는 코드를 나중에 추가한다.
    # Comment에 board_id를 나중에 추가하여 board_id를 filter로 사용한다. 접근이 제한된 게시판이나 게시물의 댓글 조회를 차단해야한다.

    filter_dict = {"id": comment_id, "post_id": post_id}

    comment = logic_get_comment(data_base=data_base, filter_dict=filter_dict)

    if comment is None:
        raise HTTPException(**http_exception_params.not_exist_resource)

    return comment
