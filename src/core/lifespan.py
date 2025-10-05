from contextlib import asynccontextmanager

from fastapi import FastAPI
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from httpx import Limits

from core.config import settings

DEEPSEEK_API_KEY = settings.DEEPSEEK.API_KEY
DEEPSEEK_TIMEOUT = settings.DEEPSEEK.TIMEOUT
DEEPSEEK_MAX_CONNECTIONS = settings.DEEPSEEK.MAX_CONNECTIONS
UNSPLASH_CLIENT_ID = settings.UNSPLASH.CLIENT_ID
UNSPLASH_TIMEOUT = settings.UNSPLASH.TIMEOUT
UNSPLASH_MAX_CONNECTIONS = settings.UNSPLASH.MAX_CONNECTIONS

deepseek_limits = Limits(max_connections=DEEPSEEK_MAX_CONNECTIONS)
unsplash_limits = Limits(max_connections=UNSPLASH_MAX_CONNECTIONS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with (
        AsyncUnsplashClient.setup(UNSPLASH_CLIENT_ID, timeout=UNSPLASH_TIMEOUT, limits=unsplash_limits),
        AsyncDeepseekClient.setup(DEEPSEEK_API_KEY, timeout=DEEPSEEK_TIMEOUT, limits=deepseek_limits),
    ):
        yield
