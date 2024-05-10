from fastapi import Request


def get_refresh_token_from_header(request: Request):
    refresh_token = request.headers.get("Authorization", "None")
    refresh_token = refresh_token.split()[-1]

    return refresh_token
