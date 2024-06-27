from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

from router.v1 import v1_router
from lifespan.lifespan import app_lifespan
from config.config import origins
from http_middleware.log_requests import log_requests

app = FastAPI(
    title="gkwk_FastAPI_toy_project",
    version="toy_project",
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
app.middleware("http")(log_requests)


app.include_router(v1_router.router)
