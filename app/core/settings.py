from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Blog API"
    debug: bool = False
    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
