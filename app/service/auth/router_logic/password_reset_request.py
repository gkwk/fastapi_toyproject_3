from fastapi import HTTPException, BackgroundTasks
from pydantic import EmailStr

from database.database import database_dependency
from exception_message import http_exception_params
from service.user.logic_get_user_with_email import logic_get_user_with_email
from service.auth.logic_smtp_send_email import logic_smtp_send_email
from auth.jwt.password_reset_token.generate_password_reset_token import (
    generate_password_reset_token,
)
from auth.jwt.password_reset_token.get_user_password_reset_token_payload import (
    get_user_password_reset_token_payload_without_path,
)
from database.redis_method import password_reset_token_cache_set
from config.config import get_settings


def password_reset_request(
    data_base: database_dependency,
    background_tasks: BackgroundTasks,
    user_email: EmailStr,
):
    user = logic_get_user_with_email(data_base=data_base, email=user_email)

    if user is None:
        raise HTTPException(**http_exception_params.not_exist_user)

    try:
        password_reset_request_token = generate_password_reset_token(
            user_id=user.id, user_role=user.role
        )
        password_reset_request_token_payload = (
            get_user_password_reset_token_payload_without_path(
                data_base=data_base, token=password_reset_request_token
            )
        )

        # 토큰은 화이트리스트 방식으로 운영한다.
        # 운영 방식에는 두가지를 생각할 수 있을 것으로 보인다.
        # 1. 사용자가 비밀번호 초기화 요청시, 기존 토큰의 존재 여부를 고려하지 않고, 새로운 토큰을 Redis에 등록한다. (key에 user_id, uuid, timestamp를 모두 기록한다.)
        # 2. 사용자가 비밀번호 초기화 요청시, 기존 토큰의 존재 여부를 고려하여, 기존 토큰을 제거하고 새로운 토큰을 Redis에 등록한다. (key에 user_id를 기록하고 value에 uuid, timestamp를 기록하여 갱신시 value만 변경한다.)
        # 현재 선택한 방식 1번.

        password_reset_token_cache_set(
            user_id=user.id,
            uuid=password_reset_request_token_payload.uuid,
            timestamp=password_reset_request_token_payload.exp,
        )

        password_reset_link = f"{get_settings().APP_DOMAIN}/api/v1/auth/password-reset/{password_reset_request_token}"

        email_subject = f"{user.name}님, 비밀번호 초기화를 위한 링크입니다."
        email_body = f"""
        <html>
            <body>
                <p>비밀번호를 초기화를 위한 링크는 다음과 같습니다.</p>
                <p><a href="{password_reset_link}">{password_reset_link}</a></p>
                <p>해당 링크로 알맞은 형태의 POST 요청을 보내주십시오.</p>
            </body>
        </html>
        """

        background_tasks.add_task(
            logic_smtp_send_email, user_email, email_subject, email_body
        )

    except HTTPException as e:
        raise e

    return password_reset_request_token_payload.uuid
