from fastapi import APIRouter

from router.v1 import v1_url

from router.v1.main import router as main_router
from router.v1.login import router as login_router
from router.v1.logout import router as logout_router
from router.v1.users import router as users_router


router = APIRouter(
    prefix=v1_url.API_V1_ROUTER_PREFIX,
)

router.include_router(main_router.router)
router.include_router(login_router.router)
router.include_router(logout_router.router)
router.include_router(users_router.router)
