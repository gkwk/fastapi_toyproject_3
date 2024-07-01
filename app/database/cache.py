from abc import ABC, abstractmethod
from typing import Any, Optional
from redis import Redis

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.database import get_data_base_decorator
from models import Board
from config.config import get_settings


class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass


class RedisCache(CacheInterface):

    def __init__(self):
        self._cache = Redis(host=get_settings().REDIS_HOST_NAME, port=6379, db=0)

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            return self._cache.get(key)
        else:
            raise HTTPException(status_code=500)

    def set(self, key: str, value: Any, kw: dict = {}) -> None:
        self._cache.set(key, value, **kw)

    def delete(self, key: str) -> None:
        self._cache.delete(key)

    def exist(self, key: str) -> bool:
        return key in self._cache


@get_data_base_decorator
def cache_init(data_base: Session, cache_interface: CacheInterface):
    get_stmt = select(Board.id, Board.is_visible)
    board_is_visible = data_base.execute(get_stmt).all()

    for id, is_visible in board_is_visible:
        cache_interface.set(f"board:{id}", int(is_visible))


in_memory_cache = RedisCache()


# memory_cache = MemoryCache()
cache_init(data_base=None, cache_interface=in_memory_cache)


def board_cache_set(board_id: int, is_visible: bool):
    in_memory_cache.set(f"board:{board_id}", int(is_visible))


def board_cache_delete(board_id: int):
    in_memory_cache.delete(f"board:{board_id}")


def board_cache_get(board_id: int):
    value: bytes = in_memory_cache.get(f"board:{board_id}")
    value = int(value.decode("utf-8"))
    value = bool(value)
    return value


def blacklisted_access_token_cache_set(user_id: int, uuid: str, timestamp: int):
    in_memory_cache.set(
        f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}",
        "",
        kw={"ex": get_settings().APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60},
    )


def blacklisted_access_token_cache_delete(user_id: int, uuid: str, timestamp: int):
    in_memory_cache.delete(f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}")


def blacklisted_access_token_cache_get(user_id: int, uuid: str, timestamp: int):
    value: bytes = in_memory_cache.get(
        f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}"
    )
    value = value.decode("utf-8")
    return value


def blacklisted_access_token_cache_exist(user_id: int, uuid: str, timestamp: int):
    return in_memory_cache.exist(
        f"blacklisted_access_token:{user_id}:{uuid}:{timestamp}"
    )
