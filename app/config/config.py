from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache


class Settings(BaseSettings):
    APP_DOMAIN: str
    APP_JWT_SECRET_KEY: str
    APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    APP_JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int
    OAUTH_TOKEN_URL: str
    PASSWORD_ALGORITHM: str

    RDBMS_DRIVER: str
    RDBMS_HOST_NAME: str
    RDBMS_USERNAME: str
    RDBMS_ROOT_PASSWORD: str
    RDBMS_PASSWORD: str
    RDBMS_DB_NAME: str

    CELERY_RESULT_BACKEND_FILE_NAME: str

    REDIS_HOST_NAME: str
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_PORT: str

    RABBITMQ_HOST_NAME: str
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_PORT: str
    FASTAPI_QUEUE_NAME: str

    MONGODB_HOST_NAME: str
    MONGODB_PORT: str
    MONGODB_USERNAME: str | None = None
    MONGODB_PASSWORD: str | None = None

    model_config = SettingsConfigDict(env_file=None, extra="ignore")


@lru_cache
def get_settings():
    return Settings()


# origins = ["http://localhost:3000", "http://127.0.0.1:3000"] # 프론트엔드가 사용하는 주소 추가
origins = ["*"]
