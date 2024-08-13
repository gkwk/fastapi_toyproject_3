from fastapi import APIRouter

from router.v1 import v1_url, v1_tags

from router.v1.main.file_download.file_id.http_get import http_get

router = APIRouter(prefix=v1_url.MAIN_FILE_DOWNLOAD_ID_ROUTER_PREFIX)

router.get(v1_url.ENDPOINT_SLASH, tags=[v1_tags.MAIN_TAG], name="File Download")(http_get)
