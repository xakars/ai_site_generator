import logging
from contextlib import asynccontextmanager

import aioboto3
from aiobotocore.config import AioConfig
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from httpx import Limits

from core.config import settings
from frontend_api.app import frontend_app

logger = logging.getLogger("uvicorn.error")

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
    session = aioboto3.Session()
    s3_config = {
        "endpoint_url": settings.S3.ENDPOINT_URL,
        "aws_access_key_id": settings.S3.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.S3.AWS_SECRET_ACCESS_KEY,
    }
    connct_config = AioConfig(
        max_pool_connections=settings.S3.MAX_POOL_CONNECTIONS,
        connect_timeout=settings.S3.CONNECT_TIMEOUT,
        read_timeout=settings.S3.READ_TIMEOUT,
    )

    async with (
        session.client('s3', **s3_config, config=connct_config) as s3_client,
        AsyncUnsplashClient.setup(UNSPLASH_CLIENT_ID, timeout=UNSPLASH_TIMEOUT, limits=unsplash_limits),
        AsyncDeepseekClient.setup(DEEPSEEK_API_KEY, timeout=DEEPSEEK_TIMEOUT, limits=deepseek_limits),
    ):
        frontend_app.state.s3_client = s3_client
        yield


app = FastAPI(lifespan=lifespan)


app.mount("/frontend-api", frontend_app)
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
