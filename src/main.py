from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get(
    "/users/me",
    summary="Получить учетные данные пользователя",
    tags=["Users"],
    )
def mock_get():
    mock_user_data = {
        "email": "example@example.com",
        "isActive": True,
        "profileId": "1",
        "registeredAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return JSONResponse(content=mock_user_data, status_code=200)


app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
