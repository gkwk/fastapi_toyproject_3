from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AIS_ROUTER_PREFIX)

from router.v1.ais.http_get import http_get
from router.v1.ais.http_post import http_post

from router.v1.ais.ai_id import router as ai_id_router

router.include_router(ai_id_router.router)
