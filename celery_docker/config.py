from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache


class Settings(BaseSettings):
    APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

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
