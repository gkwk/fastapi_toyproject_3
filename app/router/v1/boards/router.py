from typing import Union

from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.boards.http_get import http_get
from router.v1.boards.http_post import http_post
from router.v1.boards.board_id import router as id_router
from schema.boards.response_boards import ResponseBoardsForUser, ResponseBoardsForAdmin

router = APIRouter(prefix=v1_url.BOARDS_ROUTER_PREFIX)


router.get(
    v1_url.ENDPOINT,
    response_model=Union[ResponseBoardsForUser, ResponseBoardsForAdmin],
    tags=[v1_tags.BOARD_TAG],
    name="get_board_list",
)(http_get)
router.post(
    v1_url.ENDPOINT,
    status_code=status.HTTP_201_CREATED,
    tags=[v1_tags.BOARD_TAG],
    name="create_board",
)(http_post)

router.include_router(id_router.router)
