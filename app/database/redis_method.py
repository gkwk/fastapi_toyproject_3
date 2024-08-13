from typing import Any, Optional
from contextlib import contextmanager
from typing import Generator, Any
import os

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from redis import Redis
from redis.lock import Lock

from database.database import get_data_base_decorator
from models import Board
from config.config import get_settings


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
        if key in self._client:
            return self._client.get(key)
        else:
            raise HTTPException(status_code=500)

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


@get_data_base_decorator
def cache_init(data_base: Session, cache_interface: RedisHandler):
    get_stmt = select(Board.id, Board.is_visible)
    board_is_visible = data_base.execute(get_stmt).all()

    for id, is_visible in board_is_visible:
        cache_interface.set(f"board:{id}", int(is_visible))


redis_handler = RedisHandler()


cache_init(data_base=None, cache_interface=redis_handler)


def board_cache_set(board_id: int, is_visible: bool):
    redis_handler.set(f"board:{board_id}", int(is_visible))


def board_cache_delete(board_id: int):
    redis_handler.delete(f"board:{board_id}")


def board_cache_get(board_id: int):
    value: bytes = redis_handler.get(f"board:{board_id}")
    value = int(value.decode("utf-8"))
    value = bool(value)
    return value


def blacklisted_access_token_cache_set(user_id: int, uuid: str, timestamp: int):
    redis_handler.set(
        f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}",
        "",
        kw={"ex": get_settings().APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60},
    )


def blacklisted_access_token_cache_delete(user_id: int, uuid: str, timestamp: int):
    redis_handler.delete(f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}")


def blacklisted_access_token_cache_get(user_id: int, uuid: str, timestamp: int):
    value: bytes = redis_handler.get(
        f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}"
    )
    value = value.decode("utf-8")
    return value


def blacklisted_access_token_cache_exist(user_id: int, uuid: str, timestamp: int):
    return redis_handler.exist(f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}")


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


def password_reset_token_cache_set(user_id: int, uuid: str, timestamp: int):
    redis_handler.set(
        f"password_reset_token:{user_id}:{uuid}:{timestamp}",
        "",
        kw={"ex": 86400},
        # 60*60*24
    )


def password_reset_token_cache_unlink(user_id: int, uuid: str, timestamp: int):
    redis_handler.unlink(f"password_reset_token:{user_id}:{uuid}:{timestamp}")


def password_reset_token_cache_exist(user_id: int, uuid: str, timestamp: int):
    return redis_handler.exist(f"password_reset_token:{user_id}:{uuid}:{timestamp}")


def download_file_lock_cache_set(file_name: str):
    redis_handler.set(
        f"download_file_lock:{file_name}",
        "",
        kw={"ex": 30 * 24 * 60 * 60},
        # 60*60*24
    )


def download_file_lock_cache_exist(file_name: str):
    return redis_handler.exist(f"download_file_lock:{file_name}")


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
