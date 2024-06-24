from datetime import timedelta, datetime, UTC
import uuid
import jwt

from database.database import database_dependency
from config.config import get_settings

ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES
DOMAIN = get_settings().APP_DOMAIN
SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM


def generate_websocket_access_token(user_id: int, user_role: str):
    data = {
        "sub": "websocket_access_token",
        "exp": datetime.now(UTC) + timedelta(seconds=10),
        DOMAIN: True,
        "user_id": user_id,
        "role": user_role,
        "uuid": str(uuid.uuid4()),
    }

    websocket_access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return websocket_access_token
