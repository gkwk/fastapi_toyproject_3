from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.chat_session_id.http_get import http_get
from router.v1.chat_sessions.chat_session_id.http_delete import http_delete
from router.v1.chat_sessions.chat_session_id.http_patch import http_patch
from router.v1.chat_sessions.chat_session_id.chats import router as chats_router
from router.v1.chat_sessions.chat_session_id.ws import (
    router as chat_session_websocket_router,
)
from schema.chat_sessions.response_chat_session_detail import (
    ResponseChatSessionDetailForUser,
    ResponseChatSessionDetailForAdmin,
)

router = APIRouter(prefix=v1_url.CHAT_SESSIONS_ID_ROUTER_PREFIX)


router.get(
    v1_url.ENDPOINT,
    response_model=Union[
        ResponseChatSessionDetailForUser, ResponseChatSessionDetailForAdmin
    ],
    tags=[v1_tags.CHAT_SESSION_TAG],
    name="get_chat_session_detail",
)(http_get)
router.patch(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.CHAT_SESSION_TAG],
    name="update_chat_session_detail",
)(http_patch)
router.delete(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.CHAT_SESSION_TAG],
    name="delete_chat_session",
)(http_delete)

router.include_router(chats_router.router)
router.include_router(chat_session_websocket_router.router)
