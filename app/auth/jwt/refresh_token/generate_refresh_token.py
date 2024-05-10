from datetime import timedelta, datetime, UTC
import uuid
from jose import jwt


from models import User
from database.database import database_dependency
from config.config import get_settings


REFRESH_TOKEN_EXPIRE_MINUTES = get_settings().APP_JWT_REFRESH_TOKEN_EXPIRE_MINUTES
DOMAIN = get_settings().APP_DOMAIN
SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM


def generate_refresh_token(
    data_base: database_dependency,
    user: User,
):
    data = {
        "sub": "refresh_token",
        "exp": datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        DOMAIN: True,
        "user_id": user.id,
        "uuid": str(uuid.uuid4()),
    }

    refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return refresh_token
