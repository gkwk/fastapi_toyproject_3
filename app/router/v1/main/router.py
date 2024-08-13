from fastapi import APIRouter

from router.v1 import v1_url, v1_tags
from router.v1.main.http_get import http_get  # 순환 참조 오류 해결

from router.v1.main.file_download import router as file_download_router

router = APIRouter(prefix=v1_url.MAIN_ROUTER_PREFIX)

router.get(v1_url.ENDPOINT_SLASH, tags=[v1_tags.MAIN_TAG], name="Index")(http_get)

router.include_router(file_download_router.router)