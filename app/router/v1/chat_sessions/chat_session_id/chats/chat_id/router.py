from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.chat_sessions.chat_session_id.chats.chat_id.http_get import http_get
from router.v1.chat_sessions.chat_session_id.chats.chat_id.http_delete import (
    http_delete,
)
from schema.chats.response_chat_detail import (
    ResponseChatDetailForUser,
    ResponseChatDetailForAdmin,
)

router = APIRouter(prefix=v1_url.CHATS_ID_ROUTER_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseChatDetailForUser, ResponseChatDetailForAdmin],
    tags=[v1_tags.CHAT_TAG],
)(http_get)
router.delete(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.CHAT_TAG]
)(http_delete)
