from fastapi import APIRouter

from router.v1 import v1_url


router = APIRouter(prefix=v1_url.COMMENTS_ID_ROUTER_PREFIX)

from router.v1.boards.id.posts.post_id.comments.comment_id.http_get import http_get
from router.v1.boards.id.posts.post_id.comments.comment_id.http_patch import http_patch
from router.v1.boards.id.posts.post_id.comments.comment_id.http_delete import http_delete
