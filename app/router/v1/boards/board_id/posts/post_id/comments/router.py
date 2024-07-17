from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.posts.post_id.comments.http_get import http_get
from router.v1.boards.board_id.posts.post_id.comments.http_post import http_post
from router.v1.boards.board_id.posts.post_id.comments.comment_id import (
    router as comment_id_router,
)
from schema.comments.response_comments import (
    ResponseCommentsForUser,
    ResponseCommentsForAdmin,
)


router = APIRouter(prefix=v1_url.COMMENTS_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseCommentsForUser, ResponseCommentsForAdmin],
    tags=[v1_tags.COMMENT_TAG],
    name="get_comment_list",
)(http_get)

router.post(
    v1_url.ENDPOINT,
    status_code=status.HTTP_201_CREATED,
    tags=[v1_tags.COMMENT_TAG],
    name="create_comment",
)(http_post)

router.include_router(comment_id_router.router)
