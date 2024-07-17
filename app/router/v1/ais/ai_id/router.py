from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.ais.ai_id.http_get import http_get
from router.v1.ais.ai_id.http_patch import http_patch
from router.v1.ais.ai_id.http_delete import http_delete
from router.v1.ais.ai_id.ailogs import router as ailogs_router
from schema.ais.response_ai_detail import (
    ResponseAIDetailForUser,
    ResponseAIDetailForAdmin,
)

router = APIRouter(prefix=v1_url.AIS_ID_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseAIDetailForUser, ResponseAIDetailForAdmin],
    tags=[v1_tags.AI_TAG],
    name="get_ai_detail",
)(http_get)
router.patch(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.AI_TAG],
    name="update_ai_detail",
)(http_patch)
router.delete(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.AI_TAG],
    name="delete_ai",
)(http_delete)

router.include_router(ailogs_router.router)
