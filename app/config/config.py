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
    RDBMS_USERNAME_ENV: str
    RDBMS_PASSWORD_ENV: str
    RDBMS_DB_NAME: str
    REDIS_HOST_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


# origins = ["http://localhost:3000", "http://127.0.0.1:3000"] # 프론트엔드가 사용하는 주소 추가
origins = ["*"]
