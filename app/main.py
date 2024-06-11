import sys

from calendar import timegm
from datetime import datetime, UTC
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware
import uvicorn

from router.v1 import v1_router
from lifespan.lifespan import app_lifespan
from config.config import origins
from terminal_command.create_super_user import create_admin_with_terminal
from logger.logger_methods import log_before_response, log_after_response


app = FastAPI(
    lifespan=app_lifespan,
    servers=[
        # {"url": "/test", "description": "Test environment"},
        # {"url": "/", "description": "Production environment"},
    ],
    docs_url="/",
)

app.mount("/static", StaticFiles(directory="volume/staticfile"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    time = datetime.now(UTC)
    timestamp = timegm(time.utctimetuple())
    uuid = uuid4()

    timestamp_uuid = f"{timestamp}_{uuid}"

    log_before_response(request, timestamp_uuid)
    response: Response = await call_next(request)
    log_after_response(request, response, timestamp_uuid)

    return response


app.include_router(v1_router.router)


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) == 0:
        uvicorn.run("main:app", reload=True, log_level="debug", port=8080)
    else:
        if "createsuperuser" in argv:
            create_admin_with_terminal(data_base=None)
