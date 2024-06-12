from typing import Union

from fastapi import APIRouter

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.chat_session_id.chats.http_get import http_get
from router.v1.chat_sessions.chat_session_id.chats.chat_id import (
    router as chat_id_router,
)
from schema.chats.response_chats import (
    ResponseChatsForUser,
    ResponseChatsForAdmin,
)


router = APIRouter(prefix=v1_url.CHATS_ROUTER_ROUTER_PREFIX)
router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseChatsForUser, ResponseChatsForAdmin],
    tags=[v1_tags.CHAT_TAG],
)(http_get)

router.include_router(chat_id_router.router)
