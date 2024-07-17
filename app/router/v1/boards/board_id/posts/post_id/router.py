from typing import Union


from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.posts.post_id.http_get import http_get
from router.v1.boards.board_id.posts.post_id.http_delete import http_delete
from router.v1.boards.board_id.posts.post_id.http_patch import http_patch
from router.v1.boards.board_id.posts.post_id.comments import router as comments_router
from schema.posts.response_post_detail import (
    ResponsePostDetailForUser,
    ResponsePostDetailForAdmin,
)

router = APIRouter(prefix=v1_url.POSTS_ID_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponsePostDetailForUser, ResponsePostDetailForAdmin],
    tags=[v1_tags.POST_TAG],
    name="get_post_detail",
)(http_get)
router.patch(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.POST_TAG],
    name="update_post_detail",
)(http_patch)
router.delete(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.POST_TAG],
    name="delete_post",
)(http_delete)

router.include_router(comments_router.router)
