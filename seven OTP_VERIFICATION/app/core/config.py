from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = 'Otp Verification System'
    app_version: str = '1.0.0'
    debug: bool = True

    # database
    database_url: str = "sqlite:///./app.db" # for development only

    # security
    secret_key: str = "cd9de174a21b8e5ef76f993fa0806b93cb674b4f6979798a319f2b71ab3962e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30



settings = Settings()