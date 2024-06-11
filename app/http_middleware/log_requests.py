from calendar import timegm
from datetime import datetime, UTC
from uuid import uuid4

from fastapi import Request, Response

from logger.logger_methods import log_before_response, log_after_response


async def log_requests(request: Request, call_next):
    time = datetime.now(UTC)
    timestamp = timegm(time.utctimetuple())
    uuid = uuid4()

    timestamp_uuid = f"{timestamp}_{uuid}"

    log_before_response(request, timestamp_uuid)
    response: Response = await call_next(request)
    log_after_response(request, response, timestamp_uuid)

    return response


# 다른 방법 : https://stackoverflow.com/questions/62882830/fastapi-middleware-on-different-folder-not-working
