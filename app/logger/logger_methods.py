import logging

from fastapi import Request, Response
from urllib.parse import quote, urlsplit, urlunsplit

from logger.custom_logger import CustomTimedRotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
from logger.logger_setting import logger


def get_url_safe(request: Request):
    splited_url = urlsplit(str(request.url))
    path_safe = quote(splited_url.path)
    query_safe = quote(splited_url.query)
    url_safe = urlunsplit(
        (
            splited_url.scheme,
            splited_url.netloc,
            path_safe,
            query_safe,
            splited_url.fragment,
        )
    )

    return url_safe


def log_before_response(request: Request):
    log_url = get_url_safe(request=request)

    if request.headers.get("X-Real-IP"):
        logger.info(f"HTTP | {request.method} | Receiving request | {request.headers.get('X-Real-IP')} | {log_url} | {request.headers}")
    else:
        logger.info(f"HTTP | {request.method} | Receiving request | {request.client.host} | {log_url} | {request.headers}")


def log_after_response(request: Request, response: Response):
    log_url = get_url_safe(request=request)

    if request.headers.get("X-Real-IP"):
        logger.info(
        f"HTTP | {request.method} | {response.status_code} | Completed request | {request.headers.get('X-Real-IP')} | {log_url} | {request.headers}"
    )

    else:
        logger.info(
        f"HTTP | {request.method} | {response.status_code} | Completed request | {request.client.host}:{request.client.port} | {log_url} | {request.headers}"
    )


def log_message(message: str):
    logger.info(message)
