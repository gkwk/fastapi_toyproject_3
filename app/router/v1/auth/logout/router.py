from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AUTH_LOGOUT_ROUTER_PREFIX)


from router.v1.auth.logout.http_post import http_post
