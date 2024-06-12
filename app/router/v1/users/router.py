from fastapi import APIRouter
from starlette import status

from router.v1 import v1_url,v1_tags
from router.v1.users.http_get import http_get
from router.v1.users.http_post import http_post
from router.v1.users.user_id import router as id_router
from schema.users.response_users import ResponseUsers


router = APIRouter(prefix=v1_url.USERS_ROUTER_PREFIX)

router.get(v1_url.ENDPOINT, response_model=ResponseUsers, tags=[v1_tags.USER_TAG])(http_get)
router.post(v1_url.ENDPOINT, status_code=status.HTTP_201_CREATED, tags=[v1_tags.USER_TAG])(http_post)


router.include_router(id_router.router)
