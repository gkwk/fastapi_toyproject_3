from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.POSTS_ID_ROUTER_PREFIX)

from router.v1.boards.board_id.posts.post_id.http_get import http_get
from router.v1.boards.board_id.posts.post_id.http_delete import http_delete
from router.v1.boards.board_id.posts.post_id.http_patch import http_patch


from router.v1.boards.board_id.posts.post_id.comments import router as comments_router

router.include_router(comments_router.router)
