from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AIS_ID_ROUTER_PREFIX)

from router.v1.ais.ai_id.http_get import http_get
from router.v1.ais.ai_id.http_patch import http_patch
from router.v1.ais.ai_id.http_delete import http_delete

from router.v1.ais.ai_id.ailogs import router as ailogs_router


router.include_router(ailogs_router.router)
