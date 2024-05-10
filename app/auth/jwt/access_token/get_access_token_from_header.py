from fastapi import Request


def get_access_token_from_header(request: Request):
    access_token = request.headers.get("Authorization", "None")
    access_token = access_token.split()[-1]

    return access_token
