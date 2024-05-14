from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.BOARDS_ROUTER_PREFIX, tags=["boards"])

from router.v1.boards.root.http_get import http_get
from router.v1.boards.root.http_post import http_post
from router.v1.boards.id.http_get import http_get
from router.v1.boards.id.http_patch import http_patch
from router.v1.boards.id.http_delete import http_delete

