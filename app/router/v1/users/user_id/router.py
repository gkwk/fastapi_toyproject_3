from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url, v1_tags
from router.v1.users.user_id.http_get import http_get
from router.v1.users.user_id.http_patch import http_patch
from router.v1.users.user_id.http_delete import http_delete
from schema.users.response_user_detail import ResponseUserDetail


router = APIRouter(prefix=v1_url.USERS_ID_ROUTER_PREFIX)


router.get(v1_url.ENDPOINT, response_model=ResponseUserDetail, tags=[v1_tags.USER_TAG])(
    http_get
)
router.patch(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.USER_TAG]
)(http_patch)
router.delete(
    v1_url.ENDPOINT, status_code=status.HTTP_204_NO_CONTENT, tags=[v1_tags.USER_TAG]
)(http_delete)
