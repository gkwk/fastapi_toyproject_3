from typing import Annotated, Optional
import contextlib

from fastapi import Depends
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config.config import get_settings
from database.sqlite_naming_convention import (
    naming_convention as sqlite_naming_convention,
)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=sqlite_naming_convention)


engine = create_engine(
    get_settings().SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def database_engine_shutdown():
    global engine
    if engine:
        engine.dispose()


def get_data_base():
    data_base = session_local()
    try:
        yield data_base
    finally:
        data_base.close()


@contextlib.contextmanager
def get_data_base_for_decorator():
    data_base = session_local()
    try:
        yield data_base
    finally:
        data_base.close()


def get_data_base_decorator(f):
    def wrapper(data_base, *args, **kwargs):
        with get_data_base_for_decorator() as data_base:
            if "data_base" in kwargs:
                kwargs["data_base"] = data_base
            f(data_base, *args, **kwargs)

    return wrapper


database_dependency = Annotated[Session, Depends(get_data_base)]

DATABASE_DRIVER_NAME = engine.name