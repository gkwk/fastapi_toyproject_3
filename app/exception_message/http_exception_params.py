from starlette import status

http_exception_params = {
    "not_unique_user_name": {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "동일한 이름을 사용중인 사용자가 이미 존재합니다.",
    },
    "not_unique_email": {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "동일한 이메일을 사용중인 사용자가 이미 존재합니다.",
    },
    "not_exist_user": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "해당 사용자는 존재하지 않습니다.",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    "not_verified_password": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "패스워드가 일치하지 않습니다.",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    "banned_user": {
        "status_code": status.HTTP_403_FORBIDDEN,
        "detail": "해당 사용자는 차단되었습니다.",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    "not_verified_token": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "JWT Validation Error",
    },
    "already_user_name_existed": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Bad Request",
    },
    "not_exist_resource": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "해당 리소스는 존재하지 않습니다.",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    "not_unique_attribute_value": {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "변경 요청한 속성값은 이미 사용중입니다.",
    },
    "not_exist_ai_model": {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "AI 모델이 존재하지 않습니다.",
    },
}
