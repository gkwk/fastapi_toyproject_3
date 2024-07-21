from typing import Annotated

from fastapi import Path, Depends


def get_password_reset_token_from_path(password_reset_token: str = Path(...)):
    return password_reset_token

password_reset_token_dependency = Annotated[dict, Depends(get_password_reset_token_from_path)]
