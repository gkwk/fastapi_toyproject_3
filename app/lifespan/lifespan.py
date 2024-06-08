import contextlib

from fastapi import FastAPI

from database.database import database_engine_shutdown
from logger.logger_methods import log_message


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("lifespan_start")
    log_message(f"SYSTEM | app start")
    yield
    print("lifespan_shutdown")
    database_engine_shutdown()
    log_message(f"SYSTEM | database shutdown")
    log_message(f"SYSTEM | app shutdown")
