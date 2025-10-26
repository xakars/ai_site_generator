import mimetypes

import anyio
import httpx
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncPageGenerator

from core.config import settings
from core.logger import logger


async def upload_to_s3(
    s3_client,
    bucket: str,
    file_name: str,
    body: bytes,
    content_disposition: str):
    mime_type, _ = mimetypes.guess_type(file_name)
    upload_params = {
        "Bucket": bucket,
        "Key": file_name,
        "ContentType": mime_type,
        "Body": body,
        "ContentDisposition": content_disposition,
    }
    await s3_client.put_object(**upload_params)


async def generate_page(user_prompt: str, s3_client, gontenberg_client):
    try:
        generator = AsyncPageGenerator(debug_mode=settings.DEBUG_MODE)
        with anyio.CancelScope(shield=True):
            async for chunk in generator(user_prompt):
                yield chunk.encode("utf-8")
            html_code = generator.html_page.html_code.encode("utf-8")
            file_name = "mocked_html.html"
            mime_type, _ = mimetypes.guess_type(file_name)
            logger.info(f"html page generation finished - {generator.html_page.title}")
            await upload_to_s3(
                s3_client,
                bucket=settings.S3.BUCKET_NAME,
                file_name=file_name,
                body=html_code,
                content_disposition="inline",
            )

            screenshot_bytes = await ScreenshotHTMLRequest(
                index_html=html_code,
                width=settings.GOTENBERG.SCREENSHOTHTMLREQUEST_WIDTH,
                format=settings.GOTENBERG.SCREENSHOTHTMLREQUEST_FORMAT,
                wait_delay=settings.GOTENBERG.SCREENSHOTHTMLREQUEST_WAIT_DELAY,
            ).asend(gontenberg_client)

            await upload_to_s3(
                s3_client,
                bucket=settings.S3.BUCKET_NAME,
                file_name="main_page.png",
                body=screenshot_bytes,
                content_disposition="inline",
            )
    except anyio.get_cancelled_exc_class():
        raise
    except (httpx.RequestError, httpx.PoolTimeout) as e:
        logger.error(f"Error occurred while connecting -> {e}")
        return
    except GotenbergServerError as e:
        logger.error(f"Couldn't get screenshot -> {e}")
        return
    except Exception as e:
        logger.error(f"Error occurred -> {e}")
        return
