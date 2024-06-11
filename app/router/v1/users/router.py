from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.USERS_ROUTER_PREFIX)

from router.v1.users.http_get import http_get
from router.v1.users.http_post import http_post

from router.v1.users.user_id import router as id_router

router.include_router(id_router.router)