from fastapi import APIRouter

from router.v1 import v1_url
from router.v1.auth.login import router as login_router
from router.v1.auth.logout import router as logout_router
from router.v1.auth.reissue_access_token import router as reissue_access_token_router
from router.v1.auth.issue_websocket_access_token import (
    router as issue_websocket_access_token_router,
)
from router.v1.auth.password_reset import router as password_reset_router

router = APIRouter(prefix=v1_url.AUTH_ROUTER_PREFIX)


router.include_router(login_router.router)
router.include_router(logout_router.router)
router.include_router(reissue_access_token_router.router)
router.include_router(issue_websocket_access_token_router.router)
router.include_router(password_reset_router.router)
