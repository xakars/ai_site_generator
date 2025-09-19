from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserDetailsResponse(BaseModel):
    profileId: int = Field(example=1)
    username: str = Field(max_length=254, example="user123")
    email: EmailStr = Field(example="example@example.com")
    isActive: bool = Field(..., example=True)
    registeredAt: datetime = Field(example="2025-06-15T18:29:56+00:00")
    updatedAt: datetime = Field(example="2025-06-15T18:29:56+00:00")


@app.get(
    "/users/me",
    summary="Получить учетные данные пользователя",
    tags=["Users"],
    response_model=UserDetailsResponse,
    )
def mock_get():
    mock_user_data = {
        "email": "example@example.com",
        "profileId": 2,
        "isActive": True,
        "registeredAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return mock_user_data


app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
