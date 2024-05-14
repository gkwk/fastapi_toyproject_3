from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AILOGS_ROUTER_PREFIX, tags=["ailogs"])

from router.v1.ailogs.root.http_get import http_get
from router.v1.ailogs.root.http_post import http_post

