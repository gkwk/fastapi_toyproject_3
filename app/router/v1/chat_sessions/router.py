from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.CHAT_SESSIONS_ROUTER_PREFIX)

from router.v1.chat_sessions.http_get import http_get
from router.v1.chat_sessions.http_post import http_post

from router.v1.chat_sessions.chat_session_id import router as chat_session_id_router

router.include_router(chat_session_id_router.router)