from fastapi import APIRouter

from router.v1 import v1_url, v1_tags

from router.v1.main.file_download.file_id import router as file_id_router

router = APIRouter(prefix=v1_url.MAIN_FILE_DOWNLOAD_ROUTER_PREFIX)

router.include_router(file_id_router.router)