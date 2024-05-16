from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.USERS_ID_ROUTER_PREFIX)


from router.v1.users.id.http_get import http_get
from router.v1.users.id.http_patch import http_patch
from router.v1.users.id.http_delete import http_delete
