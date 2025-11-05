from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_URL: str
    API_V1_PREFIX: str = "/api/v1"
    LOGIN_ENDPOINT: str = "/login"
    ALLOWED_HOSTS: List[str] = ["*"]

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

class DevelopmentSettings(Settings):
    class Config:
        env_file = ".env"


def get_settings():
    import os
    env = os.getenv("ENV", "dev")
    return DevelopmentSettings()

settings = get_settings()
