from fastapi import APIRouter

from router.v1 import v1_url, v1_tags
from router.v1.auth.password_reset.http_post import http_post

from router.v1.auth.password_reset.password_reset_token import router as password_reset_token_router

router = APIRouter(prefix=v1_url.AUTH_PASSWORD_RESET_ROUTER_PREFIX)

router.post(v1_url.ENDPOINT, tags=[v1_tags.AUTH_TAG], name="create_password_reset_request")(http_post)

router.include_router(password_reset_token_router.router)
