from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.AIS_ROUTER_PREFIX, tags=["ais"])

from router.v1.ais.root.http_get import http_get
from router.v1.ais.root.http_post import http_post

