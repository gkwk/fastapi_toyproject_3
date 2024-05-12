import sys

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware
import uvicorn

from router.v1 import v1_router
from lifespan.lifespan import app_lifespan
from config.config import origins
from terminal_command.create_super_user import create_admin_with_terminal


app = FastAPI(
    lifespan=app_lifespan,
    servers=[
        # {"url": "/test", "description": "Test environment"},
        # {"url": "/", "description": "Production environment"},
    ],
    docs_url='/'
)

app.mount("/static", StaticFiles(directory="volume/staticfile"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router.router)


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) == 0:
        uvicorn.run("main:app", reload=True, log_level="debug")
    else:
        if "createsuperuser" in argv:
            create_admin_with_terminal(data_base=None)