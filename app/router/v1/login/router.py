from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.LOGIN_ROUTER_PREFIX, tags=["login"])


from router.v1.login.root.page import page