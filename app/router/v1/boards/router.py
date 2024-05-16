from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.BOARDS_ROUTER_PREFIX)

from router.v1.boards.http_get import http_get
from router.v1.boards.http_post import http_post

from router.v1.boards.id import router as id_router

router.include_router(id_router.router)