from datetime import timedelta, datetime, UTC
import uuid
import jwt

from database.database import database_dependency
from config.config import get_settings

ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES
DOMAIN = get_settings().APP_DOMAIN
SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM


def generate_password_reset_token(user_id: int, user_role: str):
    data = {
        "sub": "password_reset_token",
        "exp": datetime.now(UTC) + timedelta(hours=24),
        DOMAIN: True,
        "user_id": user_id,
        "role": user_role,
        "uuid": str(uuid.uuid4()),
    }

    password_reset_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return password_reset_token
