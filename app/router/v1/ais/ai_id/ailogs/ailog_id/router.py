from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.ais.ai_id.ailogs.ailog_id.http_get import http_get
from router.v1.ais.ai_id.ailogs.ailog_id.http_patch import http_patch
from router.v1.ais.ai_id.ailogs.ailog_id.http_delete import http_delete
from schema.ailogs.response_ailog_detail import (
    ResponseAIlogDetailForUser,
    ResponseAIlogDetailForAdmin,
)

router = APIRouter(prefix=v1_url.AILOGS_ID_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseAIlogDetailForUser, ResponseAIlogDetailForAdmin],
    tags=[v1_tags.AILOG_TAG],
)(http_get)
router.patch(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.AILOG_TAG]
)(http_patch)
router.delete(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.AILOG_TAG]
)(http_delete)
