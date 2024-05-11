from fastapi import HTTPException

from execption_message.http_execption_params import http_exception_params
from auth.jwt.access_token.get_user_access_token_payload import current_user_access_token_payload

def scope_checker(accees_token_payload: current_user_access_token_payload, target_scopes: list):
    accees_token_scopes_set = set(accees_token_payload.get("scopes", []))
    target_scopes_set = set(target_scopes)

    if not target_scopes_set.issubset(accees_token_scopes_set):
        raise HTTPException(**http_exception_params["not_verified_token"])
