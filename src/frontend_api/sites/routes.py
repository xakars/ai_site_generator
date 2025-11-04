
from fastapi import APIRouter, Depends, Path
from starlette.responses import StreamingResponse

from core.deps import get_gotenberg_client, get_s3_client

from .generate_html_page import generate_page
from .mocked_data import MOCKED_DATA
from .schemas import CreateSiteRequest, GeneratedSitesResponse, SiteGenerationRequest, SiteResponse

sites_router = APIRouter(prefix="/sites", tags=["Sites"])


@sites_router.get(
    "/my",
    summary="Получить список сгенерированных сайтов текущего пользователя",
    response_model=GeneratedSitesResponse,
)
def get_user_sites():
    mock_site_data = {
        "sites": [MOCKED_DATA],
    }
    return mock_site_data


@sites_router.post(
    "/create",
    summary="Создать сайт",
    response_model=SiteResponse,
)
def create_site(req: CreateSiteRequest):
    return MOCKED_DATA


@sites_router.post(
    "/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    description="Код сайта будет транслироваться стримом по мере генерации.",
)
async def generate_site(
    req: SiteGenerationRequest,
    site_id: int = Path(...),
    s3=Depends(get_s3_client),
    gontenberg_client=Depends(get_gotenberg_client),
):
    return StreamingResponse(
        content=generate_page(user_prompt=req.prompt, s3_client=s3, gontenberg_client=gontenberg_client),
        media_type="text/plain; charset=utf-8",
    )


@sites_router.get(
    "/{site_id}",
    summary="Получить сайт",
    response_model=SiteResponse,
)
def get_site(site_id: int = Path(...)):
    return MOCKED_DATA
