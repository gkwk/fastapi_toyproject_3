from pydantic import BaseModel, field_validator, EmailStr, Field


class AdminCreateEmail(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=256)

    @field_validator("email")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value
