from typing import Tuple, Dict

from starlette import status
from exception_message import http_exception_params
from database.database import DATABASE_DRIVER_NAME

unknown_driver_integrity_exception_messages = {
    ("unknown", "unknown", "unknown"): {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Unknown Driver Error",
    },
}

sql_integrity_exception_messages = {
    ("unique", " user", "email"): http_exception_params.not_unique_email,
    ("unique", " ai", "name"): http_exception_params.not_unique_attribute_value,
    ("unknown", "unknown", "unknown"): {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Unknown Error",
    },
}

integrity_exception_messages_key: Dict[str, Dict[Tuple, Dict]] = {
    "sqlite": sql_integrity_exception_messages
}


def integrity_exception_messages(
    key: Tuple, data_base_driver_name: str = DATABASE_DRIVER_NAME
):
    return integrity_exception_messages_key.get(
        data_base_driver_name, unknown_driver_integrity_exception_messages
    ).get(
        key,
        unknown_driver_integrity_exception_messages[("unknown", "unknown", "unknown")],
    )





locked_resource = {
    "status_code": status.HTTP_400_BAD_REQUEST,
    "detail": "해당 자원은 잠겨있습니다.",
}

unknown_error = {
    "status_code": status.HTTP_400_BAD_REQUEST,
    "detail": "알려지지 않은 오류가 발생하였습니다."
}