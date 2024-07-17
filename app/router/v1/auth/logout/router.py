from fastapi import APIRouter

from router.v1 import v1_url, v1_tags
from router.v1.auth.logout.http_post import http_post


router = APIRouter(prefix=v1_url.AUTH_LOGOUT_ROUTER_PREFIX)

router.post(v1_url.ENDPOINT, tags=[v1_tags.AUTH_TAG], name="logout")(http_post)
