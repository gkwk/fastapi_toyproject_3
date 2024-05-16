from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.POSTS_ROUTER_PREFIX)

# from router.v1.boards.id.http_get import http_get
# from router.v1.boards.id.http_patch import http_patch
# from router.v1.boards.id.http_delete import http_delete

