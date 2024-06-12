from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.posts.post_id.comments.comment_id.http_get import (
    http_get,
)
from router.v1.boards.board_id.posts.post_id.comments.comment_id.http_patch import (
    http_patch,
)
from router.v1.boards.board_id.posts.post_id.comments.comment_id.http_delete import (
    http_delete,
)
from schema.comments.response_post_detail import (
    ResponseCommentDetailForUser,
    ResponseCommentDetailForAdmin,
)


router = APIRouter(prefix=v1_url.COMMENTS_ID_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseCommentDetailForUser, ResponseCommentDetailForAdmin],
    tags=[v1_tags.COMMENT_TAG],
)(http_get)
router.patch(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.COMMENT_TAG]
)(http_patch)
router.delete(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.COMMENT_TAG]
)(http_delete)
