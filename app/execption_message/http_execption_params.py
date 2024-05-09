from starlette import status

http_exception_params = {
    "already_user_name_existed": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Bad Request",
    },
}