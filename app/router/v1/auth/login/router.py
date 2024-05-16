from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AUTH_LOGIN_ROUTER_PREFIX)


from router.v1.auth.login.http_post import http_post