import mimetypes

import anyio
import httpx
from html_page_generator import AsyncPageGenerator

from core.config import settings


async def generate_page(user_prompt: str, s3_client):
    try:
        generator = AsyncPageGenerator(debug_mode=settings.DEBUG_MODE)
        with anyio.CancelScope(shield=True):
            async for chunk in generator(user_prompt):
                yield chunk.encode("utf-8")
            html_code = generator.html_page.html_code.encode("utf-8")
            title = generator.html_page.title
            file_name = title + ".html"
            mime_type, _ = mimetypes.guess_type(file_name)
            upload_params = {
                "Bucket": settings.S3.BUCKET_NAME,
                "Key": file_name,
                "ContentType": mime_type,
                "Body": html_code,
                "ContentDisposition": "inline",
            }

            await s3_client.put_object(**upload_params)
            print('Файл успешно сохранён!')

    except anyio.get_cancelled_exc_class():
        raise
    except (httpx.RequestError, httpx.PoolTimeout):
        return
    except Exception as e:
        print(e)
        return
