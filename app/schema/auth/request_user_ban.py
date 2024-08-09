from pydantic import BaseModel, Field


class RequestUserBan(BaseModel):
    user_id: int = Field(ge=1)
    ban: bool = Field()
