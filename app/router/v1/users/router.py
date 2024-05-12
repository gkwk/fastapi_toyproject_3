from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.USERS_ROUTER_PREFIX, tags=["users"])


from router.v1.users.root.http_post import http_post
from router.v1.users.id.http_get import http_get
from router.v1.users.id.http_patch import http_patch