from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.CHAT_SESSIONS_ID_ROUTER_PREFIX)

from router.v1.chat_sessions.chat_session_id.http_get import http_get
from router.v1.chat_sessions.chat_session_id.http_delete import http_delete
from router.v1.chat_sessions.chat_session_id.http_patch import http_patch

# from router.v1.boards.id.posts.post_id.comments import router as comments_router
from router.v1.chat_sessions.chat_session_id.ws import router as chat_session_websocket_router


# router.include_router(comments_router.router)
router.include_router(chat_session_websocket_router.router)
