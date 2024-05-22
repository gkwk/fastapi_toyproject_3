import re
from typing import Optional, List

from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core.core_schema import ValidationInfo



class RequestAIDetailPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    description: Optional[str] = Field(None, max_length=256)
    is_visible: Optional[bool] = Field(None)
    is_available: Optional[bool] = Field(None)
