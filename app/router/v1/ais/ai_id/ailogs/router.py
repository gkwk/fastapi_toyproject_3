from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.ais.ai_id.ailogs.http_get import http_get
from router.v1.ais.ai_id.ailogs.http_post import http_post
from router.v1.ais.ai_id.ailogs.ailog_id import router as ailog_id_router
from schema.ailogs.response_ailogs import ResponseAIlogsForUser, ResponseAIlogsForAdmin


router = APIRouter(prefix=v1_url.AILOGS_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseAIlogsForUser, ResponseAIlogsForAdmin],
    tags=[v1_tags.AILOG_TAG],
)(http_get)
router.post(
    v1_url.ENDPOINT, status_code=status.HTTP_202_ACCEPTED, tags=[v1_tags.AILOG_TAG]
)(http_post)

router.include_router(ailog_id_router.router)
