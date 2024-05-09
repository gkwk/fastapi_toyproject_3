from router.v1 import v1_url
from router.v1.main.router import router


@router.get(v1_url.MAIN_ROOT)
def page():
    return {"message": "Hello, FastAPI!"}
