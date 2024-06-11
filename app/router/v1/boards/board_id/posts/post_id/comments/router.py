from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.COMMENTS_ROUTER_PREFIX)

from router.v1.boards.board_id.posts.post_id.comments.http_get import http_get
from router.v1.boards.board_id.posts.post_id.comments.http_post import http_post

from router.v1.boards.board_id.posts.post_id.comments.comment_id import router as comment_id_router

router.include_router(comment_id_router.router)