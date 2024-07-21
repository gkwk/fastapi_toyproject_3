from fastapi import APIRouter
from starlette import status


from router.v1 import v1_url, v1_tags
from router.v1.auth.password_reset.password_reset_token.http_patch import http_patch


router = APIRouter(prefix=v1_url.AUTH_PASSWORD_RESET_TOKEN_ROUTER_PREFIX)

router.patch(
    v1_url.ENDPOINT,
    tags=[v1_tags.AUTH_TAG],
    status_code=status.HTTP_204_NO_CONTENT,
    name="password_reset",
)(http_patch)
