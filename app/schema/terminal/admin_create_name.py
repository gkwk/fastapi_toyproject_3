from pydantic import BaseModel, field_validator, Field

name_regex = "^[a-zA-Z][A-Za-z\d_]{0,63}$"


class AdminCreateName(BaseModel):
    name: str = Field(min_length=1, max_length=64, pattern=name_regex)

    @field_validator("name")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value
