from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.MAIN_ROUTER_PREFIX, tags=["main"])


from router.v1.main.root.http_get import http_get # 순환 참조 오류 해결