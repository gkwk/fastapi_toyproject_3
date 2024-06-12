from fastapi import APIRouter

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.chat_session_id.ws.http_get import http_get
from router.v1.chat_sessions.chat_session_id.ws.websocket_chat_session import (
    websocket_chat_session,
)


router = APIRouter(prefix=v1_url.CHAT_SESSIONS_ID_WEBSOCKET_PREFIX)

router.get(v1_url.ENDPOINT, tags=[v1_tags.CHAT_SESSION_TAG])(http_get)
router.websocket(v1_url.ENDPOINT)(websocket_chat_session)
