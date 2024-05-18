from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.POSTS_ROUTER_PREFIX)

from router.v1.boards.id.posts.http_get import http_get
from router.v1.boards.id.posts.http_post import http_post


