from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.CHATS_ID_ROUTER_ROUTER_PREFIX)

from router.v1.chat_sessions.chat_session_id.chats.chat_id.http_get import http_get
from router.v1.chat_sessions.chat_session_id.chats.chat_id.http_delete import (
    http_delete,
)
