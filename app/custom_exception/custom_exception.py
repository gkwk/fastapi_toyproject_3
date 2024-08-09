from fastapi import HTTPException


class NotExistUserHTTPException(HTTPException):
    pass


class BannedUserHTTPException(HTTPException):
    pass

class InvalidTokenErrorHTTPException(HTTPException):
    pass