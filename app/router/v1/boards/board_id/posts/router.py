from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.posts.http_get import http_get
from router.v1.boards.board_id.posts.http_post import http_post
from router.v1.boards.board_id.posts.post_id import router as post_id_router
from schema.posts.response_posts import ResponsePostsForUser, ResponsePostsForAdmin


router = APIRouter(prefix=v1_url.POSTS_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponsePostsForUser, ResponsePostsForAdmin],
    tags=[v1_tags.POST_TAG],
)(http_get)
router.post(
    v1_url.ENDPOINT, status_code=status.HTTP_201_CREATED, tags=[v1_tags.POST_TAG]
)(http_post)


router.include_router(post_id_router.router)
