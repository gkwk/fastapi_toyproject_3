import contextlib

from fastapi import FastAPI

from database.database import database_engine_shutdown


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("lifespan_start")
    yield
    print("lifespan_shutdown")
    database_engine_shutdown()