from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.LOGOUT_ROUTER_PREFIX, tags=["logout"])


from router.v1.logout.root.page import page