from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AUTH_REISSUE_ACCESS_TOKEN_ROUTER_PREFIX)


from router.v1.auth.reissue_access_token.http_get import http_get
