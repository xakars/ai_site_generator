from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DseekSettings(BaseModel):
    API_KEY: SecretStr = Field(description="Your API Key")
    MAX_CONNECTIONS: int = Field(gt=0, description="Maximum number of connections")
    TIMEOUT: int = Field(gt=0, description="Connection timeout")


class UnsplashSettings(BaseModel):
    CLIENT_ID: SecretStr = Field(description="Your Client ID")
    MAX_CONNECTIONS: int = Field(gt=0, description="Maximum number of connections")
    TIMEOUT: int = Field(gt=0, description="Connection timeout")


class S3ClientSettings(BaseModel):
    ENDPOINT_URL: str = Field(description="Url")
    AWS_ACCESS_KEY_ID: str = Field(description="MINIO_ROOT_USER")
    AWS_SECRET_ACCESS_KEY: str = Field(description="MINIO_ROOT_PASSWORD")
    BUCKET_NAME: str = Field(description="Bucket name")
    MAX_POOL_CONNECTIONS: int = Field(qt=0, description="Max pool connections")
    CONNECT_TIMEOUT: int = Field(qt=0, description="Time to connecting")
    READ_TIMEOUT: int = Field(qt=0, description="Time to read data")


class Settings(BaseSettings):
    DEEPSEEK: DseekSettings
    UNSPLASH: UnsplashSettings
    S3: S3ClientSettings
    DEBUG_MODE: bool = Field(default=False, description="Debug mode to see dseek model working on terminal")
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="forbid",
    )


settings = Settings()
