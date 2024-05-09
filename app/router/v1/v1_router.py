from fastapi import APIRouter

from router.v1 import v1_url

from router.v1.main import router as main_router

router = APIRouter(
    prefix=v1_url.API_V1_ROUTER_PREFIX,
)

router.include_router(main_router.router)