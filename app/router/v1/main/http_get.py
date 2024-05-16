from router.v1 import v1_url, v1_tags
from router.v1.main.router import router


@router.get(v1_url.ENDPOINT_SLASH, tags=[v1_tags.MAIN_TAG])
def http_get():
    return {"message": "Hello, FastAPI!"}
