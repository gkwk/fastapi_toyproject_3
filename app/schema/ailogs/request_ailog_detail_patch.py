import re
from typing import Optional, List

from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core.core_schema import ValidationInfo



class RequestAIlogDetailPatch(BaseModel):
    description: Optional[str] = Field(None, max_length=256)