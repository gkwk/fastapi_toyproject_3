from typing import Any, Optional
from contextlib import contextmanager
from typing import Generator, Any
import os

from redis import Redis
from redis.lock import Lock

from test.celery_test.config import get_settings


class RedisHandler:
    def __init__(self):
        self._client = Redis(
            host=get_settings().REDIS_HOST_NAME,
            port=get_settings().REDIS_PORT,
            db=0,
            password=get_settings().REDIS_PASSWORD,
            username=get_settings().REDIS_USERNAME,
        )

    def get(self, key: str) -> Optional[Any]:
        return self._client.get(key)

    def set(self, key: str, value: Any, kw: dict = {}) -> None:
        self._client.set(key, value, **kw)

    def delete(self, key: str | list) -> None:
        self._client.delete(key)

    def exist(self, key: str) -> bool:
        return key in self._client

    def unlink(self, key: str | list) -> None:
        self._client.unlink(key)

    def scan(self, match: str, count) -> Generator[bytes, None, None]:
        cursor = 0
        while True:
            cursor, keys = self._client.scan(cursor=cursor, match=match, count=count)
            for key in keys:
                yield key

            if cursor == 0:
                break

    def close(self):
        if self._client:
            self._client.close()


redis_handler = RedisHandler()


def post_view_count_cache_set(
    user_id: int, post_id, uuid: str, timestamp: int, value: str = "1"
):
    redis_handler.set(f"post_view_count:{user_id}:{post_id}:{uuid}:{timestamp}", value)


def post_view_count_cache_unlink(user_id: int, post_id, uuid: str, timestamp: int):
    redis_handler.unlink(f"post_view_count:{user_id}:{post_id}:{uuid}:{timestamp}")


def post_view_count_cache_get(user_id: int, post_id, uuid: str, timestamp: int) -> int:
    value: bytes = redis_handler.get(
        f"post_view_count:{user_id}:{post_id}:{uuid}:{timestamp}"
    )
    value = int(value.decode("utf-8"))
    return value


def post_view_count_cache_exist(user_id: int, post_id, uuid: str, timestamp: int):
    return redis_handler.exist(
        f"post_view_count:{user_id}:{post_id}:{uuid}:{timestamp}"
    )


def post_view_count_cache_scan(count=10):
    for key in redis_handler.scan(match="post_view_count:*", count=count):
        yield key


@contextmanager
def redis_lock(lock_name, timeout=60):
    lock: Lock = redis_handler._client.lock(f"redis_lock:{lock_name}", timeout=timeout)
    try:
        yield lock.acquire(blocking=True)
    finally:
        try:
            lock.release()
        except:
            pass
