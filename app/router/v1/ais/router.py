from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.ais.http_get import http_get
from router.v1.ais.http_post import http_post
from router.v1.ais.ai_id import router as ai_id_router
from schema.ais.response_ais import ResponseAIsForUser, ResponseAIsForAdmin


router = APIRouter(prefix=v1_url.AIS_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseAIsForUser, ResponseAIsForAdmin],
    tags=[v1_tags.AI_TAG],
)(http_get)
router.post(
    v1_url.ENDPOINT, status_code=status.HTTP_202_ACCEPTED, tags=[v1_tags.AI_TAG]
)(http_post)

router.include_router(ai_id_router.router)
