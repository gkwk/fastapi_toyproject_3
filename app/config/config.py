from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache


class Settings(BaseSettings):
    APP_DOMAIN: str
    APP_JWT_SECRET_KEY: str
    APP_JWT_EXPIRE_MINUTES: int
    PASSWORD_ALGORITHM: str
    SQLALCHEMY_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


# origins = ["http://localhost:3000", "http://127.0.0.1:3000"] # 프론트엔드가 사용하는 주소 추가
origins = ["*"]
