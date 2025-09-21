import asyncio
import os

from fastapi import HTTPException


async def generate_html(file_path: str):
    if not os.path.abspath(file_path).startswith("/Users/arsenhakimov/Documents/2dvmn/ai_site_generator/src/static"):
        raise HTTPException(status_code=400, detail="Invalid file path")

    with open(file_path, "r", encoding="utf-8") as file:  # noqa: UP015
        for line in file:
            await asyncio.sleep(0.1)
            yield line.encode("utf-8")
