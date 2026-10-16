from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from patas_backend.auth.dependencies import get_current_user
from patas_backend.models.user import User

router = APIRouter()


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    is_platform_admin: bool


@router.get("/me", response_model=UserResponse)
async def me(user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_platform_admin=user.is_platform_admin,
    )
