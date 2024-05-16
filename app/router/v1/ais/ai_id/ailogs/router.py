from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AILOGS_ROUTER_PREFIX)

from router.v1.ais.ai_id.ailogs.http_get import http_get
from router.v1.ais.ai_id.ailogs.http_post import http_post
