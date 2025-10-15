import json

from fastapi import APIRouter, Depends, Path
from starlette.responses import StreamingResponse

from core.deps import get_s3_client

from .generate_html_chunks import generate_page
from .schemas import CreateSiteRequest, GeneratedSitesResponse, SiteGenerationRequest, SiteResponse

with open("/home/ars/Documents/2devman/ai_site_generator/src/frontend_api/sites/mocked_data.json", encoding="utf-8") as f:
    data = json.load(f)
sites_router = APIRouter(prefix="/sites", tags=["Sites"])


@sites_router.get(
    "/my",
    summary="Получить список сгенерированных сайтов текущего пользователя",
    tags=["Sites"],
    response_model=GeneratedSitesResponse,
)
def get_user_sites():
    mock_site_data = {
        "sites": [data],
    }

    return mock_site_data


@sites_router.post(
    "/create",
    summary="Создать сайт",
    tags=["Sites"],
    response_model=SiteResponse,
)
def create_site(req: CreateSiteRequest):
    return data


@sites_router.post(
    "/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    description="Код сайта будет транслироваться стримом по мере генерации.",
    tags=["Sites"],
)
async def generate_site(
    req: SiteGenerationRequest,
    site_id: int = Path(...),
    s3=Depends(get_s3_client),
):
    return StreamingResponse(
        content=generate_page(user_prompt=req.prompt, s3_client=s3),
        media_type="text/plain; charset=utf-8",
    )


@sites_router.get(
    "/{site_id}",
    summary="Получить сайт",
    tags=["Sites"],
    response_model=SiteResponse,
)
def get_site(site_id: int = Path(...)):
    return data
