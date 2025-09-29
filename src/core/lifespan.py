from contextlib import asynccontextmanager

from fastapi import FastAPI
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient

from core.config import settings

DEEPSEEK_API_KEY = settings.DEEPSEEK.API_KEY.get_secret_value()
UNSPLASH_CLIENT_ID = settings.UNSPLASH.CLIENT_ID.get_secret_value()
TIMEOUT = settings.UNSPLASH.TIMEOUT


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with (
        AsyncUnsplashClient.setup(UNSPLASH_CLIENT_ID, timeout=TIMEOUT),
        AsyncDeepseekClient.setup(DEEPSEEK_API_KEY),
    ):
        yield
