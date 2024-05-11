from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.USERS_ROUTER_PREFIX, tags=["users"])


from app.router.v1.users.root.http_post import http_post