from fastapi import HTTPException
from app.core.dependency import get_current_user
from app.services.auth_service import AuthService
from app.schemas.user.user import UpdateUser
from app.schemas.user.user import UserProfileResponse
from app.models.user_model import User
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency.get_db import get_db
from app.utils.common_response import APIResponse
from app.services.user_service import UserService


user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/", response_model=APIResponse[list[UserProfileResponse]])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    users = await service.get_all_users()
    return APIResponse(success=True, message="Users fetched successfully", data=users)

@user_router.get("/{user_id}", response_model=APIResponse[UserProfileResponse])
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_user_by_id(user_id)
    return APIResponse(success=True, message="User fetched successfully", data=user)

@user_router.get("/email/{email}", response_model=APIResponse[UserProfileResponse])
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_user_by_email(email)
    return APIResponse(success=True, message="User fetched successfully", data=user)

@user_router.get("/username/{username}", response_model=APIResponse[UserProfileResponse])
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_user_by_username(username)
    return APIResponse(success=True, message="User fetched successfully", data=user)

@user_router.put("/{user_id}", response_model=APIResponse[UserProfileResponse])
async def update_user(user_id: int, data: UpdateUser, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = UserService(db)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")

    user = await service.update_user(user_id, data)
    return APIResponse(success=True, message="User updated successfully", data=user)

@user_router.delete("/{user_id}", response_model=APIResponse[None])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = UserService(db)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")

    await service.delete_user(user_id)
    return APIResponse(success=True, message="User deleted successfully", data=None)
