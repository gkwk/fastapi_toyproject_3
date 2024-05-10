from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.JOIN_ROUTER_PREFIX, tags=["join"])


from router.v1.join.root.page import page