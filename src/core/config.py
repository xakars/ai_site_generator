from pydantic import BaseModel, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DseekSettings(BaseModel):
    API_KEY: SecretStr
    MAX_CONNECTIONS: PositiveInt = None
    TIMEOUT: PositiveInt = None


class UnsplashSettings(BaseModel):
    CLIENT_ID: SecretStr
    MAX_CONNECTIONS: PositiveInt = None
    TIMEOUT: PositiveInt = None


class Settings(BaseSettings):
    DEEPSEEK: DseekSettings
    UNSPLASH: UnsplashSettings
    DEBUG_MODE: bool = False
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="forbid",
    )


settings = Settings()
