import aiofiles
import anyio
import httpx
from html_page_generator import AsyncPageGenerator

from core.config import settings

file_path = "/home/ars/Documents/2devman/ai_site_generator/src/static/"


async def generate_page(user_prompt: str):
    try:
        generator = AsyncPageGenerator(debug_mode=settings.DEBUG_MODE)
        with anyio.CancelScope(shield=True):
            async for chunk in generator(user_prompt):
                yield chunk.encode("utf-8")
            async with aiofiles.open(file_path + 'testHTML.html', 'w') as f:
                await f.write(generator.html_page.html_code)
            print('Файл успешно сохранён!')

    except anyio.get_cancelled_exc_class():
        raise
    except (httpx.RequestError, httpx.PoolTimeout):
        return
    except Exception as e:
        print(e)
        return
