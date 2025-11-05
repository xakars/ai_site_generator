from contextlib import asynccontextmanager

import aioboto3
import httpx
from aiobotocore.config import AioConfig
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from httpx import Limits

from core.config import settings
from frontend_api.app import frontend_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = aioboto3.Session()
    s3_config = {
        "endpoint_url": str(settings.S3.ENDPOINT_URL),
        "aws_access_key_id": settings.S3.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.S3.AWS_SECRET_ACCESS_KEY,
    }
    connect_config = AioConfig(
        max_pool_connections=settings.S3.MAX_POOL_CONNECTIONS,
        connect_timeout=settings.S3.CONNECT_TIMEOUT,
        read_timeout=settings.S3.READ_TIMEOUT,
    )

    async with (
        AsyncUnsplashClient.setup(
            settings.UNSPLASH.CLIENT_ID,
            timeout=settings.UNSPLASH.TIMEOUT,
            limits=Limits(max_connections=settings.UNSPLASH.MAX_CONNECTIONS)),
        AsyncDeepseekClient.setup(
            settings.DEEPSEEK.API_KEY,
            timeout=settings.DEEPSEEK.TIMEOUT,
            limits=Limits(max_connections=settings.DEEPSEEK.MAX_CONNECTIONS)),
        session.client('s3', **s3_config, config=connect_config) as s3_client,
        httpx.AsyncClient(
            base_url=str(settings.GOTENBERG.URL),
            timeout=settings.GOTENBERG.TIMEOUT,
        ) as gotenberg_client,

    ):
        frontend_app.state.s3_client = s3_client
        frontend_app.state.gotenberg_client = gotenberg_client
        yield


app = FastAPI(lifespan=lifespan)


app.mount("/frontend-api", frontend_app) # frontend_app is a sub-app to isolate frontend logic
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
