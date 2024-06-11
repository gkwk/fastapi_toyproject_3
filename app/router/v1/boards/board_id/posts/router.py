from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.POSTS_ROUTER_PREFIX)

from router.v1.boards.board_id.posts.http_get import http_get
from router.v1.boards.board_id.posts.http_post import http_post

from router.v1.boards.board_id.posts.post_id import router as post_id_router

router.include_router(post_id_router.router)
