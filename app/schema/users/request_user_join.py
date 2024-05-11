import re

from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core.core_schema import ValidationInfo

name_regex = "^[a-zA-Z][A-Za-z\d_]{0,63}$"

password_regex = (
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$@!%&*?])[A-Za-z\d#$@!%&*?]{8,32}$"
)


class RequestUserJoin(BaseModel):
    name: str = Field(min_length=1, max_length=64, pattern=name_regex)
    password1: str = Field(min_length=8, max_length=32)
    password2: str = Field(min_length=8, max_length=32)
    email: EmailStr = Field(min_length=1, max_length=256)

    @field_validator("name", "password1", "password2", "email")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value

    @field_validator("password2")
    def password_confirm(cls, value, info: ValidationInfo):
        if "password1" in info.data and value != info.data["password1"]:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return value

    @field_validator("password1", "password2")
    def is_password_proper(cls, value: str):
        if not re.match(password_regex, value):
            raise ValueError(
                "소문자, 대문자, 숫자, 특수문자(#$@!%&*?) 들이 모두 최소 한번씩 사용되어야 합니다."
            )
        return value
