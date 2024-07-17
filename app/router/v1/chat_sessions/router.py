from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.http_get import http_get
from router.v1.chat_sessions.http_post import http_post
from router.v1.chat_sessions.chat_session_id import router as chat_session_id_router
from schema.chat_sessions.response_chat_sessions import (
    ResponseChatSessionsForUser,
    ResponseChatSessionsForAdmin,
)

router = APIRouter(prefix=v1_url.CHAT_SESSIONS_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseChatSessionsForUser, ResponseChatSessionsForAdmin],
    tags=[v1_tags.CHAT_SESSION_TAG],
    name="get_chat_session_list",
)(http_get)
router.post(
    v1_url.ENDPOINT,
    status_code=status.HTTP_201_CREATED,
    tags=[v1_tags.CHAT_SESSION_TAG],
    name="create_chat_session",
)(http_post)

router.include_router(chat_session_id_router.router)
