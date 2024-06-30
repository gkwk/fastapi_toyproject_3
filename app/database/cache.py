from abc import ABC, abstractmethod
from typing import Any, Optional
import threading

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.database import get_data_base_decorator
from models import Board


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


class InMemoryCache(CacheInterface):
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        # if self._lock.acquire(timeout=5):
        #     try:
        #         if key in self._cache:
        #             return self._cache.get(key)
        #         else:
        #             raise HTTPException(status_code=500)
        #     finally:
        #         self._lock.release()
        # else:
        #     raise HTTPException(status_code=500)
        if key in self._cache:
            return self._cache.get(key)
        else:
            raise HTTPException(status_code=500)

    def set(self, key: str, value: Any) -> None:
        if self._lock.acquire(timeout=5):
            try:
                self._cache[key] = value
            finally:
                self._lock.release()
        else:
            raise HTTPException(status_code=500)

    def delete(self, key: str) -> None:
        if self._lock.acquire(timeout=5):
            try:
                self._cache.pop(key, None)
            finally:
                self._lock.release()
        else:
            raise HTTPException(status_code=500)


@get_data_base_decorator
def cache_init(data_base: Session, cache_interface: CacheInterface):
    get_stmt = select(Board.id, Board.is_visible)
    board_is_visible = data_base.execute(get_stmt).all()

    for id, is_visible in board_is_visible:
        cache_interface.set(f"board:{id}", is_visible)


def board_cache_set(board_id: int, is_visible: bool):
    in_memory_cache.set(f"board:{board_id}", is_visible)


def board_cache_delete(board_id: int):
    in_memory_cache.delete(f"board:{board_id}")


def board_cache_get(board_id: int):
    return in_memory_cache.get(f"board:{board_id}")


in_memory_cache = InMemoryCache()
cache_init(data_base=None, cache_interface=in_memory_cache)
