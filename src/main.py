
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from apps.sites_sub_app import app_sites
from apps.users_sub_app import app_users


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
print(settings.model_dump())


app = FastAPI()


app.mount("/sites", app_sites)
app.mount("/users", app_users)
app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
