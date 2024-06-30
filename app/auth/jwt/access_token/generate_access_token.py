from datetime import timedelta, datetime, UTC
import uuid
import jwt

from sqlalchemy import select

from database.database import database_dependency
from models import User, UserPermissionTable
from config.config import get_settings

ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES
DOMAIN = get_settings().APP_DOMAIN
SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM


def generate_access_token(data_base: database_dependency, user: User):
    get_stmt = select(UserPermissionTable.board_id).where(
        UserPermissionTable.user_id == user.id
    )
    
    scopes = data_base.execute(statement=get_stmt).scalars().all()

    data = {
        "sub": "access_token",
        "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        DOMAIN: True,
        "user_name": user.name,
        "user_id": user.id,
        "role": user.role,
        "uuid": str(uuid.uuid4()),
        "scope": scopes,
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return access_token
