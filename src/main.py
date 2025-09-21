
from datetime import datetime

from fastapi import FastAPI, Path
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field

from tools.generate_html_chunks import generate_html

app = FastAPI()


class UserDetailsResponse(BaseModel):
    profileId: int = Field(example=1)
    username: str = Field(max_length=254, example="user123")
    email: EmailStr = Field(example="example@example.com")
    isActive: bool = Field(..., example=True)
    registeredAt: datetime = Field(example="2025-06-15T18:29:56+00:00")
    updatedAt: datetime = Field(example="2025-06-15T18:29:56+00:00")


class CreateSiteRequest(BaseModel):
    prompt: str = Field(..., example="Сайт любителей играть в домино")
    title: str | None = Field(None, max_length=128, example="Фан клуб игры в домино")


class SiteResponse(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="Фан клуб Домино")
    htmlCodeUrl: str | None = Field(..., example="http://example.com/media/index.html")
    htmlCodeDownloadUrl: str | None = Field(..., example="http://example.com/media/index.html?response-content-disposition=attachment")
    screenshotUrl: str | None = Field(..., example="http://example.com/media/index.png")
    prompt: str = Field(..., example="Сайт любителей играть в домино")
    createdAt: datetime = Field(..., example="2025-06-15T18:29:56+00:00")
    updatedAt: datetime = Field(..., example="2025-06-15T18:29:56+00:00")


class SiteGenerationRequest(BaseModel):
    prompt: str | None = Field(..., example="Сайт любителей играть в домино")


class GeneratedSitesResponse(BaseModel):
    sites: list[SiteResponse]


@app.get(
    "/users/me",
    summary="Получить учетные данные пользователя",
    tags=["Users"],
    response_model=UserDetailsResponse,
    )
def get_user():
    mock_user_data = {
        "email": "example@example.com",
        "profileId": 2,
        "isActive": True,
        "registeredAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return mock_user_data


@app.get(
    "/sites/my",
    summary="Получить список сгенерированных сайтов текущего пользователя",
    tags=["Sites"],
    response_model=GeneratedSitesResponse,
)
def get_user_sites():
    mock_site_data = {
        "sites": [{
        "id": 1,
        "title": "Фан клуб Домино",
        "htmlCodeUrl": "https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html",
        "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
        "screenshotUrl": "http://example.com/media/index.png",
        "prompt": "Сайт любителей играть в домино",
        "createdAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }],
    }

    return mock_site_data


@app.post(
    "/sites/create",
    summary="Создать сайт",
    tags=["Sites"],
    response_model=SiteResponse,
)
def create_site(req: CreateSiteRequest):
    mock_site_data = {
        "id": 1,
        "title": "Фан клуб Домино",
        "htmlCodeUrl": "http://example.com/media/index.html",
        "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
        "screenshotUrl": "http://example.com/media/index.png",
        "prompt": "Сайт любителей играть в домино",
        "createdAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return mock_site_data


@app.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    description="Код сайта будет транслироваться стримом по мере генерации.",
    tags=["Sites"],
)
def generate_site(
    req: SiteGenerationRequest,
    site_id: int = Path(...),
):
    file_path = "/Users/arsenhakimov/Documents/2dvmn/ai_site_generator/src/static/testHTML.html"
    return StreamingResponse(content=generate_html(file_path), media_type="text/plain; charset=utf-8")


@app.get(
    "/sites/{site_id}",
    summary="Получить сайт",
    tags=["Sites"],
    response_model=SiteResponse,
)
def get_site(site_id: int = Path(...)):
    mock_site_data = {
        "id": 1,
        "title": "Фан клуб Домино",
        "htmlCodeUrl": "https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html",
        "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
        "screenshotUrl": "http://example.com/media/index.png",
        "prompt": "Сайт любителей играть в домино",
        "createdAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return mock_site_data


app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
