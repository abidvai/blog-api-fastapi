from app.schemas.auth.refresh_token_schemas import RefreshToken
from app.schemas.auth.user_create_schemas import UserCreate
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency.get_db import get_db
from app.schemas.auth.login import LoginUser
from app.schemas.token_response import TokenResponse
from app.utils.common_response import APIResponse
from app.services.auth_service import AuthService


auth_route = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_route.post("/login", response_model=APIResponse[TokenResponse])
async def login(data: LoginUser, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    token_data = await service.login(data)
    return APIResponse(success=True, message="Login successful", data=token_data)

@auth_route.post("/register", response_model=APIResponse[TokenResponse])
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    token_data = await service.register(data)
    return APIResponse(success=True, message="Register successful", data=token_data)

@auth_route.post("/refresh", response_model=APIResponse[TokenResponse])
async def refresh(data: RefreshToken, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    token_data = await service.refresh(data)
    return APIResponse(success=True, message="Token refreshed successfully", data=token_data)

@auth_route.post("/logout", response_model=APIResponse[None])
async def logout(token: str, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    await service.logout(token)
    return APIResponse(success=True, message="Logout successful", data=None)

    


