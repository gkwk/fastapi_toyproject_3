from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.COMMENTS_ID_ROUTER_PREFIX)

# from router.v1.boards.id.posts.post_id.
# from router.v1.boards.id.posts.post_id.
