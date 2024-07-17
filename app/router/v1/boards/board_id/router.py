from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.board_id.http_get import http_get
from router.v1.boards.board_id.http_patch import http_patch
from router.v1.boards.board_id.http_delete import http_delete
from router.v1.boards.board_id.posts import router as posts_router
from schema.boards.response_board_detail import (
    ResponseBoardDetailForUser,
    ResponseBoardDetailForAdmin,
)

router = APIRouter(prefix=v1_url.BOARDS_ID_ROUTER_PREFIX)

router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseBoardDetailForUser, ResponseBoardDetailForAdmin],
    tags=[v1_tags.BOARD_TAG],
    name="get_board_detail",
)(http_get)
router.patch(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.BOARD_TAG],
    name="update_board_detail",
)(http_patch)
router.delete(
    v1_url.ENDPOINT,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[v1_tags.BOARD_TAG],
    name="delete_board",
)(http_delete)


router.include_router(posts_router.router)
