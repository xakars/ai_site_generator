from datetime import datetime

from pydantic import AnyUrl, BaseModel, EmailStr, Field


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
    htmlCodeUrl: AnyUrl | None = Field(..., example="http://example.com/media/index.html")
    htmlCodeDownloadUrl: AnyUrl | None = Field(..., example="http://example.com/media/index.html?response-content-disposition=attachment")
    screenshotUrl: AnyUrl | None = Field(..., example="http://example.com/media/index.png")
    prompt: str = Field(..., example="Сайт любителей играть в домино")
    createdAt: datetime = Field(..., example="2025-06-15T18:29:56+00:00")
    updatedAt: datetime = Field(..., example="2025-06-15T18:29:56+00:00")


class SiteGenerationRequest(BaseModel):
    prompt: str | None = Field(..., example="Сайт любителей играть в домино")


class GeneratedSitesResponse(BaseModel):
    sites: list[SiteResponse]
