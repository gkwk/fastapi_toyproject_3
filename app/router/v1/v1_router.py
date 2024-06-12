from fastapi import APIRouter

from router.v1 import v1_url
from router.v1.main import router as main_router
from router.v1.auth import router as auth_router
from router.v1.users import router as users_router
from router.v1.boards import router as boards_router
from router.v1.ais import router as ais_router
from router.v1.chat_sessions import router as chat_sessions_router

router = APIRouter(
    prefix=v1_url.API_V1_ROUTER_PREFIX,
)

router.include_router(main_router.router)
router.include_router(auth_router.router)
router.include_router(users_router.router)
router.include_router(boards_router.router)
router.include_router(ais_router.router)
router.include_router(chat_sessions_router.router)
