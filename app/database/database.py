from typing import Annotated, Optional
import contextlib
import functools
import os

from fastapi import Depends
from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config.config import get_settings
from database.sqlite_naming_convention import (
    naming_convention as sqlite_naming_convention,
)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=sqlite_naming_convention)


def register_foreign_keys(engine):
    """register PRAGMA foreign_keys=on on connection"""

    @event.listens_for(engine, "connect")
    def connect(dbapi_con, con_record):
        cursor = dbapi_con.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


RDB_PATH_URL = ""
if get_settings().RDBMS_DRIVER == "mysql":
    RDB_PATH_URL = f"mysql+pymysql://{get_settings().RDBMS_USERNAME}:{get_settings().RDBMS_PASSWORD}@{get_settings().RDBMS_HOST_NAME}/{get_settings().RDBMS_DB_NAME}"
else:
    RDB_PATH_URL = f"sqlite:///./volume/database/{get_settings().RDBMS_DB_NAME}.sqlite"

connect_args = {}

if RDB_PATH_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(RDB_PATH_URL, connect_args=connect_args)
if RDB_PATH_URL.startswith("sqlite"):
    register_foreign_keys(engine)


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


def get_data_base_decorator_v2(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with get_data_base_for_decorator() as data_base:
            f(*args, data_base=data_base, **kwargs)

    return wrapper


database_dependency = Annotated[Session, Depends(get_data_base)]

DATABASE_DRIVER_NAME = engine.name
