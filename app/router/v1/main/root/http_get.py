from router.v1 import v1_url
from router.v1.main.router import router


@router.get(v1_url.MAIN_ROOT)
def http_get():
    return {"message": "Hello, FastAPI!"}
