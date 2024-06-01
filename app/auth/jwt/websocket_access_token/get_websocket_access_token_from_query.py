from typing import Annotated

from fastapi import Query, Depends


def get_websocket_access_token_from_query(websocket_access_token: str = Query(None)):
    return websocket_access_token

websocket_access_token_dependency = Annotated[dict, Depends(get_websocket_access_token_from_query)]
