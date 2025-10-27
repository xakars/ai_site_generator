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
    ENDPOINT_URL: str = Field(description="URL address of the S3 server")
    AWS_ACCESS_KEY_ID: str = Field(description="MINIO_ROOT_USER")
    AWS_SECRET_ACCESS_KEY: str = Field(description="MINIO_ROOT_PASSWORD")
    BUCKET_NAME: str = Field(description="Bucket name")
    MAX_POOL_CONNECTIONS: int = Field(qt=0, description="Max pool connections")
    CONNECT_TIMEOUT: int = Field(qt=0, description="Time to connecting")
    READ_TIMEOUT: int = Field(qt=0, description="Time to read data")


class GotenbergSettings(BaseModel):
    URL: str = Field(description="URL address of the Gotenberg server")
    SCREENSHOTHTMLREQUEST_WIDTH: int = Field(description="Width of screenshot")
    SCREENSHOTHTMLREQUEST_FORMAT: str = Field(description="Format of screenshot")
    SCREENSHOTHTMLREQUEST_WAIT_DELAY: int = Field(description="Delay in seconds while animation in html will be wait")
    TIMEOUT: int = Field(gt=0, description="Connection timeout")


class Settings(BaseSettings):
    DEEPSEEK: DseekSettings
    UNSPLASH: UnsplashSettings
    S3: S3ClientSettings
    GOTENBERG: GotenbergSettings
    DEBUG_MODE: bool = Field(default=False, description="Debug mode to see dseek model working on terminal")
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
