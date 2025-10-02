from fastapi import APIRouter

from .schemas import UserDetailsResponse

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "/me",
    summary="Получить учетные данные пользователя",
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
