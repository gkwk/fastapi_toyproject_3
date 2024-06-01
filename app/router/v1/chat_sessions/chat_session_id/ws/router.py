from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.CHAT_SESSIONS_ID_WEBSOCKET_PREFIX)

from router.v1.chat_sessions.chat_session_id.ws.http_get import http_get
from router.v1.chat_sessions.chat_session_id.ws.websocket_chat_session import websocket_chat_session
