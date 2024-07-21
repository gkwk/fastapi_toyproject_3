from pydantic import BaseModel, EmailStr, Field


class RequestPasswordResetRequest(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=256)
